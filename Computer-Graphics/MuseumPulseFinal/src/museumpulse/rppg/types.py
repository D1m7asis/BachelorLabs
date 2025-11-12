from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class ROIResult:
    """Result of ROI detection for a single frame."""

    frame_size: Tuple[int, int]
    face_bbox: Optional[Tuple[int, int, int, int]]
    forehead_bbox: Optional[Tuple[int, int, int, int]]


@dataclass
class PulseReading:
    """Represents a single BPM estimate and its diagnostics."""

    timestamp: float
    bpm: Optional[float]
    raw_bpm: Optional[float]
    snr: Optional[float]
    quality: str
    status: str
    window_duration: float

    def to_message(self) -> dict:
        """Return a JSON serialisable payload."""

        return {
            "timestamp": self.timestamp,
            "bpm": self.bpm,
            "raw_bpm": self.raw_bpm,
            "snr": self.snr,
            "quality": self.quality,
            "status": self.status,
            "window_duration": self.window_duration,
        }
