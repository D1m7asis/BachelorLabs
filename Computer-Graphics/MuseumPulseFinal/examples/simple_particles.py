"""Простейшая визуализация BPM в виде пульсирующих частиц.

Запуск:
    pip install pygame websockets
    python simple_particles.py --uri ws://localhost:8765/
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import random
from dataclasses import dataclass
from typing import List

import pygame
import websockets


@dataclass
class Particle:
    angle: float
    radius: float
    speed: float

    def update(self, bpm: float, dt: float) -> None:
        self.angle += self.speed * dt
        base = 40 + bpm * 0.5
        self.radius = base + 20 * math.sin(self.angle)


class ParticleField:
    def __init__(self, count: int = 64) -> None:
        self.particles: List[Particle] = [
            Particle(angle=random.random() * math.tau, radius=50.0, speed=1.0 + random.random())
            for _ in range(count)
        ]

    def update(self, bpm: float, dt: float) -> None:
        for particle in self.particles:
            particle.update(bpm, dt)

    def draw(self, screen: pygame.Surface, bpm: float) -> None:
        width, height = screen.get_size()
        center = (width // 2, height // 2)
        color_intensity = min(255, max(0, int(80 + bpm)))
        screen.fill((10, 10, 20))
        for particle in self.particles:
            offset_x = int(math.cos(particle.angle) * particle.radius)
            offset_y = int(math.sin(particle.angle) * particle.radius)
            radius = max(2, int(2 + bpm / 30))
            pygame.draw.circle(
                screen,
                (color_intensity, 120, 255 - color_intensity // 2),
                (center[0] + offset_x, center[1] + offset_y),
                radius,
                width=0,
            )


async def consume(uri: str, field: ParticleField) -> None:
    async with websockets.connect(uri) as ws:
        async for message in ws:
            data = json.loads(message)
            bpm = data.get("bpm") or 60.0
            field.update(bpm, dt=0.0)  # immediate update on message


async def main(uri: str) -> None:
    pygame.init()
    pygame.display.set_caption("Museum Pulse Visualisation")
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    field = ParticleField()

    bpm_value = 60.0

    async def ws_task() -> None:
        nonlocal bpm_value
        async with websockets.connect(uri) as ws:
            async for message in ws:
                data = json.loads(message)
                bpm_value = data.get("bpm") or bpm_value

    consumer = asyncio.create_task(ws_task())

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dt = clock.tick(60) / 1000.0
            field.update(bpm_value, dt)
            field.draw(screen, bpm_value)
            pygame.display.flip()
            await asyncio.sleep(0)
    finally:
        consumer.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await consumer
        pygame.quit()


if __name__ == "__main__":
    import contextlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", default="ws://localhost:8765/", help="WebSocket URI")
    args = parser.parse_args()
    asyncio.run(main(args.uri))
