from __future__ import annotations

import asyncio
import json
import logging
from typing import Optional, Set

import websockets
from websockets import WebSocketServerProtocol

from ..rppg.types import PulseReading

LOGGER = logging.getLogger(__name__)


class BPMWebSocketServer:
    """Simple WebSocket broadcaster for BPM readings."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8765) -> None:
        self.host = host
        self.port = port
        self._server: Optional[websockets.server.Serve] = None
        self._connections: Set[WebSocketServerProtocol] = set()
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        LOGGER.info("Starting WebSocket server on %s:%d", self.host, self.port)
        self._server = await websockets.serve(self._handler, self.host, self.port)

    async def stop(self) -> None:
        if self._server is not None:
            LOGGER.info("Stopping WebSocket server")
            self._server.close()
            await self._server.wait_closed()
            self._server = None

    async def _handler(self, websocket: WebSocketServerProtocol) -> None:
        LOGGER.info("Client connected: %s", websocket.remote_address)
        async with self._lock:
            self._connections.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            async with self._lock:
                self._connections.discard(websocket)
            LOGGER.info("Client disconnected: %s", websocket.remote_address)

    async def broadcast(self, reading: PulseReading) -> None:
        message = json.dumps(reading.to_message())
        async with self._lock:
            connections = list(self._connections)
        if not connections:
            return
        websockets.broadcast(connections, message)
