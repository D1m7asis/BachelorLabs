from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional
import numpy as np

import cv2

from ..rppg.types import PulseReading, ROIResult

LOGGER = logging.getLogger(__name__)


@dataclass
class PanelConfig:
    enabled: bool = True
    window_name: str = "Museum Pulse Monitor"


class ServicePanel:
    """Overlay diagnostics on top of the camera feed."""

    def __init__(self, config: Optional[PanelConfig] = None) -> None:
        self.config = config or PanelConfig()
        self._headless = False
        if self.config.enabled:
            try:
                cv2.namedWindow(self.config.window_name, cv2.WINDOW_NORMAL)
            except cv2.error as exc:  # pragma: no cover - OpenCV runtime specific
                LOGGER.warning("Failed to create OpenCV window: %s", exc)
                self._headless = True

    def show(self, frame: np.ndarray, roi: ROIResult, reading: PulseReading) -> bool:
        if not self.config.enabled or self._headless:
            return True

        display = frame.copy()
        if roi.face_bbox:
            x, y, w, h = roi.face_bbox
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 255), 2)
        if roi.forehead_bbox:
            fx, fy, fw, fh = roi.forehead_bbox
            cv2.rectangle(display, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)

        overlay_lines = [
            f"BPM: {reading.bpm:.1f}" if reading.bpm is not None else "BPM: --",
            f"Raw: {reading.raw_bpm:.1f}" if reading.raw_bpm is not None else "Raw: --",
            f"SNR: {reading.snr:.2f} dB" if reading.snr is not None else "SNR: --",
            f"Quality: {reading.quality}",
            f"Status: {reading.status}",
        ]
        y0 = 30
        for line in overlay_lines:
            cv2.putText(display, line, (10, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y0 += 30

        cv2.imshow(self.config.window_name, display)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            LOGGER.info("Quit signal received from service panel")
            return False
        return True

    def close(self) -> None:
        if self.config.enabled and not self._headless:
            cv2.destroyWindow(self.config.window_name)
