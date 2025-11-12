from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Deque, Optional, Tuple

import numpy as np
from collections import deque

from .quality import classify_quality
from .roi import FaceROIExtractor
from .signal_processing import estimate_bpm
from .types import PulseReading, ROIResult

LOGGER = logging.getLogger(__name__)


@dataclass
class DetectorConfig:
    window_seconds: float = 30.0
    min_window_seconds: float = 15.0
    bpm_range: Tuple[float, float] = (45.0, 160.0)
    bpm_smoothing: float = 0.8
    max_jump_bpm: float = 12.0
    min_snr_db: float = 1.5


@dataclass
class DetectorState:
    timestamps: Deque[float] = field(default_factory=lambda: deque(maxlen=900))
    values: Deque[float] = field(default_factory=lambda: deque(maxlen=900))
    last_timestamp: float = 0.0
    smoothed_bpm: Optional[float] = None


class PulseDetector:
    """Extracts rPPG signals from video frames and computes BPM estimates."""

    def __init__(self, config: Optional[DetectorConfig] = None) -> None:
        self.config = config or DetectorConfig()
        self.state = DetectorState()
        self.roi_extractor = FaceROIExtractor()

    def process_frame(self, frame: np.ndarray, timestamp: float) -> Tuple[PulseReading, ROIResult]:
        roi = self.roi_extractor.detect(frame)

        if roi.forehead_bbox is None:
            reading = PulseReading(
                timestamp=timestamp,
                bpm=None,
                raw_bpm=None,
                snr=None,
                quality="unknown",
                status="no-face",
                window_duration=0.0,
            )
            return reading, roi

        patch = self.roi_extractor.extract_patch(frame, roi.forehead_bbox)
        green_channel = patch[:, :, 1]
        value = float(np.mean(green_channel))

        self.state.timestamps.append(timestamp)
        self.state.values.append(value)
        self.state.last_timestamp = timestamp

        # Remove samples outside the sliding window
        while self.state.timestamps and timestamp - self.state.timestamps[0] > self.config.window_seconds:
            self.state.timestamps.popleft()
            self.state.values.popleft()

        window_duration = (
            self.state.timestamps[-1] - self.state.timestamps[0]
            if len(self.state.timestamps) > 1
            else 0.0
        )

        if window_duration < self.config.min_window_seconds:
            reading = PulseReading(
                timestamp=timestamp,
                bpm=None,
                raw_bpm=None,
                snr=None,
                quality="warming-up",
                status="insufficient-window",
                window_duration=window_duration,
            )
            return reading, roi

        values_array = np.array(self.state.values, dtype=np.float64)
        timestamps_array = np.array(self.state.timestamps, dtype=np.float64)

        raw_bpm, snr = estimate_bpm(values_array, timestamps_array, self.config.bpm_range)
        quality = classify_quality(snr)

        smoothed_bpm = self._smooth_bpm(raw_bpm)
        status = self._classify_status(raw_bpm, smoothed_bpm, snr)

        reading = PulseReading(
            timestamp=timestamp,
            bpm=smoothed_bpm,
            raw_bpm=raw_bpm,
            snr=snr,
            quality=quality,
            status=status,
            window_duration=window_duration,
        )
        return reading, roi

    def reset(self) -> None:
        self.state = DetectorState()

    def _smooth_bpm(self, bpm: Optional[float]) -> Optional[float]:
        if bpm is None:
            self.state.smoothed_bpm = None
            return None

        if self.state.smoothed_bpm is None:
            self.state.smoothed_bpm = bpm
        else:
            alpha = float(np.clip(self.config.bpm_smoothing, 0.0, 0.99))
            delta = bpm - self.state.smoothed_bpm
            max_delta = max(self.config.max_jump_bpm, 0.0)
            if max_delta > 0 and abs(delta) > max_delta:
                delta = np.sign(delta) * max_delta
            self.state.smoothed_bpm = self.state.smoothed_bpm + (1.0 - alpha) * delta
        return self.state.smoothed_bpm

    def _classify_status(
        self,
        raw_bpm: Optional[float],
        smoothed_bpm: Optional[float],
        snr: Optional[float],
    ) -> str:
        if raw_bpm is None or smoothed_bpm is None:
            return "unstable"

        if snr is None or snr < self.config.min_snr_db:
            return "low-snr"

        if abs(raw_bpm - smoothed_bpm) > self.config.max_jump_bpm * 0.75:
            return "jump-suppressed"

        return "ok"
