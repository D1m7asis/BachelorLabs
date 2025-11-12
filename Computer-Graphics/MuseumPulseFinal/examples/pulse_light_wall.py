"""Визуализация «Pulse Light Wall»: световая панель мерцает в такт BPM.

Запуск:
    pip install pygame websockets
    python pulse_light_wall.py --uri ws://localhost:8765/
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import math
import random
from dataclasses import dataclass
from typing import Tuple

import pygame
import websockets


@dataclass
class LightCell:
    x: int
    y: int
    size: int
    phase_offset: float

    def draw(self, surface: pygame.Surface, color: Tuple[int, int, int], intensity: float) -> None:
        fade = max(0.0, min(1.0, intensity))
        r = int(color[0] * fade)
        g = int(color[1] * fade)
        b = int(color[2] * fade)
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, (r, g, b), rect)
        border_colour = (min(255, r + 40), min(255, g + 40), min(255, b + 40))
        pygame.draw.rect(surface, border_colour, rect, width=max(1, self.size // 16))


def generate_grid(width: int, height: int, cols: int, rows: int) -> list[LightCell]:
    margin_x = width * 0.08
    margin_y = height * 0.12
    usable_w = width - margin_x * 2
    usable_h = height - margin_y * 2
    cell_w = usable_w / cols
    cell_h = usable_h / rows
    size = int(min(cell_w, cell_h) * 0.9)

    cells: list[LightCell] = []
    for row in range(rows):
        for col in range(cols):
            x = int(margin_x + col * cell_w + (cell_w - size) / 2)
            y = int(margin_y + row * cell_h + (cell_h - size) / 2)
            phase_offset = random.random() * math.tau
            cells.append(LightCell(x=x, y=y, size=size, phase_offset=phase_offset))
    return cells


def bpm_to_color(bpm: float) -> Tuple[int, int, int]:
    min_bpm, max_bpm = 50.0, 140.0
    t = (bpm - min_bpm) / (max_bpm - min_bpm)
    t = max(0.0, min(1.0, t))
    # Синий (спокойствие) → Красный (возбуждение)
    blue = (30, 80, 210)
    red = (240, 40, 40)
    r = int(blue[0] + (red[0] - blue[0]) * t)
    g = int(blue[1] + (red[1] - blue[1]) * t)
    b = int(blue[2] + (red[2] - blue[2]) * t)
    return r, g, b


async def run_visualisation(uri: str) -> None:
    pygame.init()
    screen = pygame.display.set_mode((960, 540))
    pygame.display.set_caption("Museum Pulse — Pulse Light Wall")
    clock = pygame.time.Clock()

    bpm_value = 62.0
    grid = generate_grid(*screen.get_size(), cols=10, rows=5)
    global_phase = 0.0

    async def websocket_consumer() -> None:
        nonlocal bpm_value
        async with websockets.connect(uri) as ws:
            async for message in ws:
                data = json.loads(message)
                bpm = data.get("bpm") or data.get("raw_bpm")
                if bpm:
                    bpm_value = max(40.0, min(180.0, float(bpm)))

    consumer_task = asyncio.create_task(websocket_consumer())

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dt = clock.tick(60) / 1000.0
            frequency = max(0.5, min(3.0, bpm_value / 60.0))
            global_phase += frequency * dt * math.tau
            colour = bpm_to_color(bpm_value)

            screen.fill((5, 5, 12))
            for cell in grid:
                pulse = (math.sin(global_phase + cell.phase_offset * 0.6) + 1.0) / 2.0
                flare = 0.65 + pulse * 0.35
                cell.draw(screen, colour, flare)

            pygame.display.flip()
            await asyncio.sleep(0)
    finally:
        consumer_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await consumer_task
        pygame.quit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", default="ws://localhost:8765/", help="WebSocket URI")
    args = parser.parse_args()
    asyncio.run(run_visualisation(args.uri))


if __name__ == "__main__":
    main()
