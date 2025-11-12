from __future__ import annotations

import logging
from typing import Optional

from pythonosc import udp_client

from ..rppg.types import PulseReading

LOGGER = logging.getLogger(__name__)


class OSCBroadcaster:
    """Broadcast BPM updates over OSC."""

    def __init__(self, host: str = "127.0.0.1", port: int = 9000, address: str = "/bpm") -> None:
        self.host = host
        self.port = port
        self.address = address
        self._client: Optional[udp_client.SimpleUDPClient] = None

    def connect(self) -> None:
        LOGGER.info("Initialising OSC client %s:%d", self.host, self.port)
        self._client = udp_client.SimpleUDPClient(self.host, self.port)

    def close(self) -> None:
        self._client = None

    def send(self, reading: PulseReading) -> None:
        if self._client is None:
            return
        if reading.bpm is None:
            return
        payload = [reading.bpm]
        LOGGER.debug("Sending OSC payload %s to %s", payload, self.address)
        self._client.send_message(self.address, payload)
