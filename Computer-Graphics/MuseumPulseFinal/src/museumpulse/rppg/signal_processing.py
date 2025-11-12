from __future__ import annotations

import logging

import numpy as np
from scipy import signal

LOGGER = logging.getLogger(__name__)


def detrend_signal(values: np.ndarray) -> np.ndarray:
    """Remove the linear trend from the signal."""

    return signal.detrend(values)


def bandpass_filter(values: np.ndarray, fps: float, low: float = 0.7, high: float = 4.0) -> np.ndarray:
    """Apply a Butterworth bandpass filter in the physiological range."""

    if fps <= 0:
        raise ValueError("Sampling frequency must be positive")
    nyquist = 0.5 * fps
    low_norm = max(low / nyquist, 0.001)
    high_norm = min(high / nyquist, 0.999)
    b, a = signal.butter(3, [low_norm, high_norm], btype="band")
    pad_need = 3 * max(len(a), len(b))

    # filtfilt требует достаточную длину сигнала; иначе – мягкий фоллбэк
    if values.size > pad_need:
        return signal.filtfilt(b, a, values)

    return signal.lfilter(b, a, values)


def compute_periodogram(values: np.ndarray, fps: float) -> Tuple[np.ndarray, np.ndarray]:
    """Return frequency and power spectral density of the signal."""

    freqs, power = signal.periodogram(values, fs=fps, detrend=False, window="hann")
    return freqs, power


def estimate_bpm(
    values: np.ndarray,
    timestamps: np.ndarray,
    bpm_range: Tuple[float, float] = (45.0, 180.0),
) -> Tuple[Optional[float], Optional[float]]:
    """Compute BPM and SNR from the preprocessed signal."""

    if len(values) < 10:
        return None, None

    duration = timestamps[-1] - timestamps[0]
    if duration <= 0:
        return None, None

    # Resample to a uniform grid for spectral analysis.
    fps = len(values) / duration
    uniform_time = np.linspace(timestamps[0], timestamps[-1], len(values))
    resampled = np.interp(uniform_time, timestamps, values)

    filtered = bandpass_filter(detrend_signal(resampled), fps)
    freqs, power = compute_periodogram(filtered, fps)

    low_hz = bpm_range[0] / 60.0
    high_hz = bpm_range[1] / 60.0
    mask = (freqs >= low_hz) & (freqs <= high_hz)

    if not np.any(mask):
        return None, None

    freq_band = freqs[mask]
    power_band = power[mask]

    peak_idx = np.argmax(power_band)
    peak_freq = freq_band[peak_idx]
    bpm = peak_freq * 60.0

    # Signal-to-noise ratio: dominant peak vs. remainder of the spectrum.
    peak_power = power_band[peak_idx]
    noise_power = np.sum(power_band) - peak_power
    if noise_power <= 0:
        snr = None
    else:
        snr = 10 * np.log10(peak_power / (noise_power / (len(power_band) - 1)))

    return float(bpm), snr
