from __future__ import annotations

import asyncio
import logging
from typing import Any, Coroutine

import websockets
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedError

from .dispatchers import BaseDispatcher

from aioretry import (
    RetryPolicy,
    RetryInfo,
    retry
)

# from sdk.client import BaseDispatcher


logger = logging.getLogger('async_websocket_client')
MSG_PREFIX = "[AioWebsocket] "
ATOM_RETRY_DELAY = 0.3
MAX_RETRIES_BEFORE_RESET = 10


def DEFAULT_RETRY_POLICY(info: RetryInfo) -> RetryPolicyStrategy:
    return (
        False,
        (info.fails - 1) % MAX_RETRIES_BEFORE_RESET * ATOM_RETRY_DELAY
    )


class AsyncWebSocketApp(object):
    url: str
    dispatcher: BaseDispatcher
    ws: WebSocketClientProtocol

    is_running: bool

    def __init__(self, url: str, dispatcher: BaseDispatcher):
        self.url = url
        self.dispatcher = dispatcher
        self.dispatcher.set_app(self)
        self._retry_policy: RetryPolicy = DEFAULT_RETRY_POLICY
        self.is_running = False

    async def connect(self):
        await self.dispatcher.before_connect()
        self.ws = await websockets.connect(self.url)
        await self.dispatcher.set_websocket(self.ws)
        await self.dispatcher.on_connect()

        self.is_running = True

    async def disconnect(self):
        self.is_running = False

        await self.dispatcher.before_disconnect()
        await self.ws.close()
        await self.dispatcher.on_disconnect()

    async def send(self, message: str) -> Any:
        return await self.ws.send(message)

    async def ws_recv_message(self) -> str | None:
        try:
            return await asyncio.wait_for(self.ws.recv(), 1)

        except asyncio.TimeoutError:
            return None

    async def ws_recv_loop(self):
        while self.is_running:
            message = await self.ws.recv()
            if message is None:
                continue

            await self.dispatcher.on_message(message)

    @retry(
        retry_policy='_retry_policy',
        before_retry='_reconnect'
    )
    async def run(self):
        await self.connect()

        try:
            await self.ws_recv_loop()

        except asyncio.exceptions.CancelledError as ex:
            logger.error([type(ex), ex])

        except ConnectionClosedError as e:
            # logger.error(f'Connection closed with error: {e}')
            await self.disconnect()
            raise e

    async def _reconnect(self, info: RetryInfo) -> None:
        logger.error(
            format_msg(
                f'socket error {info.exception}, reconnecting {info.fails}...',
            )
        )

    def asyncio_run(self):
        try:
            asyncio.run(self.run())

        except KeyboardInterrupt:
            logger.info('Correct exit')


def format_msg(string, *args) -> str:
    return MSG_PREFIX + string % args


def repr_exception(e: Exception) -> str:
    """Better stringify an exception
    """

    s = str(e)
    class_name = type(e).__name__

    return class_name if not s else f'{class_name}: {s}'
