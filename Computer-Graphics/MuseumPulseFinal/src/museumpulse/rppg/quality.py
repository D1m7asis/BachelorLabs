from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SignalQualityThresholds:
    """Thresholds controlling the classification of signal quality."""

    snr_good: float = 6.0
    snr_ok: float = 3.0


def classify_quality(snr: Optional[float]) -> str:
    if snr is None:
        return "unknown"
    if snr >= SignalQualityThresholds.snr_good:
        return "good"
    if snr >= SignalQualityThresholds.snr_ok:
        return "moderate"
    return "poor"
