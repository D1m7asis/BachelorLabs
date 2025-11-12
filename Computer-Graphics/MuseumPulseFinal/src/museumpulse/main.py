from __future__ import annotations

import argparse
import asyncio
import logging
import time
from pathlib import Path

import cv2

from museumpulse.rppg.detector import PulseDetector, DetectorConfig
from museumpulse.transport.osc_sender import OSCBroadcaster
from museumpulse.transport.websocket_server import BPMWebSocketServer
from museumpulse.ui.service_panel import PanelConfig, ServicePanel
from museumpulse.utils.data_logger import PulseDataLogger
from museumpulse.utils.logging import set_verbosity

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Museum Pulse: rPPG-based BPM monitor")
    parser.add_argument("--source", default=0, help="Camera index or video file path")
    parser.add_argument("--width", type=int, default=1280, help="Capture width")
    parser.add_argument("--height", type=int, default=720, help="Capture height")
    parser.add_argument("--websocket-port", type=int, default=8765, help="WebSocket port")
    parser.add_argument("--osc-port", type=int, default=9000, help="OSC UDP port")
    parser.add_argument("--osc-host", default="127.0.0.1", help="OSC target host")
    parser.add_argument("--no-osc", action="store_true", help="Disable OSC broadcasting")
    parser.add_argument("--no-websocket", action="store_true", help="Disable WebSocket server")
    parser.add_argument("--no-ui", action="store_true", help="Disable OpenCV service panel")
    parser.add_argument("--log", type=Path, default=None, help="Path to CSV log file")
    parser.add_argument("--verbose", action="count", default=0, help="Increase logging verbosity")
    parser.add_argument(
        "--window",
        type=float,
        default=30.0,
        help="Sliding window size in seconds for BPM estimation",
    )
    parser.add_argument(
        "--min-window",
        type=float,
        default=15.0,
        help="Minimum filled window duration before reporting BPM",
    )
    parser.add_argument(
        "--bpm-range",
        type=float,
        nargs=2,
        default=(45.0, 160.0),
        metavar=("BPM_MIN", "BPM_MAX"),
        help="Physiological BPM range",
    )
    return parser.parse_args()


def create_capture(source: str, width: int, height: int) -> cv2.VideoCapture:
    if source.isdigit():
        source_idx = int(source)
    else:
        source_idx = source
    cap = cv2.VideoCapture(source_idx)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap


async def run_monitor(args: argparse.Namespace) -> None:
    set_verbosity(args.verbose)
    detector = PulseDetector(
        DetectorConfig(
            window_seconds=args.window,
            min_window_seconds=args.min_window,
            bpm_range=tuple(args.bpm_range),
        )
    )
    panel = ServicePanel(PanelConfig(enabled=not args.no_ui))
    logger = PulseDataLogger(args.log) if args.log else None

    osc = OSCBroadcaster(host=args.osc_host, port=args.osc_port)
    if not args.no_osc:
        osc.connect()

    ws_server = BPMWebSocketServer(port=args.websocket_port)
    if not args.no_websocket:
        await ws_server.start()

    cap = create_capture(str(args.source), args.width, args.height)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open capture source {args.source}")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                LOGGER.warning("Frame grab failed; attempting to recover")
                await asyncio.sleep(0.1)
                continue

            timestamp = time.time()
            reading, roi = detector.process_frame(frame, timestamp)

            if logger:
                logger.write(reading)

            if not args.no_websocket:
                await ws_server.broadcast(reading)

            if not args.no_osc:
                osc.send(reading)

            if not panel.show(frame, roi, reading):
                break

            await asyncio.sleep(0)
    finally:
        cap.release()
        panel.close()
        if logger:
            logger.close()
        if not args.no_websocket:
            await ws_server.stop()
        if not args.no_osc:
            osc.close()


def main() -> None:
    args = parse_args()
    asyncio.run(run_monitor(args))


if __name__ == "__main__":
    main()
