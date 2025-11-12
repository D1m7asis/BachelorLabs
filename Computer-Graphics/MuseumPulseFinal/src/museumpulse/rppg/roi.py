from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import numpy as np

from .types import ROIResult

LOGGER = logging.getLogger(__name__)


@dataclass
class FaceROIConfig:
    """Configuration for selecting regions of interest on the face."""

    min_face_size: Tuple[int, int] = (120, 120)
    scale_factor: float = 1.1
    min_neighbors: int = 5
    forehead_fraction: Tuple[float, float, float, float] = (0.3, 0.05, 0.4, 0.18)
    stabilization_alpha: float = 0.75
    """Exponential smoothing factor for stabilising the face bounding box (0-1)."""

    max_drift: float = 25.0
    """Maximum number of pixels the stabilised ROI can move between frames."""
    """
    x, y, width, height fractions relative to the face bounding box.
    Tuned to focus on the central forehead region where specular highlights are lower
    and pulsatile signal is strong.
    """


class FaceROIExtractor:
    """Detects facial ROI suitable for rPPG signal extraction."""

    def __init__(self, config: Optional[FaceROIConfig] = None) -> None:
        self.config = config or FaceROIConfig()
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            raise RuntimeError(f"Failed to load Haar cascade from {cascade_path}")
        self._smoothed_face: Optional[np.ndarray] = None

    def detect(self, frame: np.ndarray) -> ROIResult:
        """Locate the face and forehead ROI on the current frame."""

        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.config.scale_factor,
            minNeighbors=self.config.min_neighbors,
            minSize=self.config.min_face_size,
        )

        if len(faces) == 0:
            LOGGER.debug("No face detected in frame")
            return ROIResult(frame_size=(width, height), face_bbox=None, forehead_bbox=None)

        # Choose the largest detected face (closest to the camera)
        x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
        stabilised = self._stabilise_face(np.array([x, y, w, h], dtype=np.float32), frame.shape)
        sx, sy, sw, sh = stabilised
        forehead = self._forehead_roi(sx, sy, sw, sh)

        return ROIResult(
            frame_size=(width, height),
            face_bbox=(int(sx), int(sy), int(sw), int(sh)),
            forehead_bbox=forehead,
        )

    def _forehead_roi(self, x: int, y: int, w: int, h: int) -> Optional[Tuple[int, int, int, int]]:
        fx, fy, fw, fh = self.config.forehead_fraction
        roi_x = int(x + w * fx)
        roi_y = int(y + h * fy)
        roi_w = int(w * fw)
        roi_h = int(h * fh)
        if roi_w <= 0 or roi_h <= 0:
            return None
        return roi_x, roi_y, roi_w, roi_h

    def _stabilise_face(self, bbox: np.ndarray, frame_shape: Tuple[int, int, int]) -> Tuple[int, int, int, int]:
        """Apply exponential smoothing and displacement limiting to the detected face."""

        alpha = float(np.clip(self.config.stabilization_alpha, 0.0, 0.99))
        if self._smoothed_face is None:
            self._smoothed_face = bbox
        else:
            drift = bbox[:2] - self._smoothed_face[:2]
            drift_norm = float(np.linalg.norm(drift))
            if self.config.max_drift > 0 and drift_norm > self.config.max_drift:
                drift = drift * (self.config.max_drift / drift_norm)
                bbox[:2] = self._smoothed_face[:2] + drift
            self._smoothed_face = alpha * self._smoothed_face + (1.0 - alpha) * bbox

        x, y, w, h = self._smoothed_face
        frame_h, frame_w = frame_shape[:2]
        w = np.clip(w, self.config.min_face_size[0], frame_w)
        h = np.clip(h, self.config.min_face_size[1], frame_h)
        x = np.clip(x, 0, max(0, frame_w - w))
        y = np.clip(y, 0, max(0, frame_h - h))
        return int(x), int(y), int(w), int(h)

    @staticmethod
    def extract_patch(frame: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        x, y, w, h = bbox
        return frame[y : y + h, x : x + w]
