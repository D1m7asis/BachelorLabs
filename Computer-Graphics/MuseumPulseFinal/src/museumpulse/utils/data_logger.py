from __future__ import annotations

import csv
import logging
from pathlib import Path
from ..rppg.types import PulseReading

LOGGER = logging.getLogger(__name__)


class PulseDataLogger:
    """Persist BPM readings with diagnostics for later analysis."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self._file = log_path.open("w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        self._writer.writerow(["timestamp", "bpm", "raw_bpm", "snr", "quality", "status", "window_sec"])
        LOGGER.info("Logging BPM data to %s", log_path)

    def write(self, reading: PulseReading) -> None:
        self._writer.writerow(
            [
                f"{reading.timestamp:.3f}",
                f"{reading.bpm:.2f}" if reading.bpm is not None else "",
                f"{reading.raw_bpm:.2f}" if reading.raw_bpm is not None else "",
                f"{reading.snr:.2f}" if reading.snr is not None else "",
                reading.quality,
                reading.status,
                f"{reading.window_duration:.2f}",
            ]
        )
        self._file.flush()

    def close(self) -> None:
        LOGGER.info("Closing BPM logger")
        self._file.close()
