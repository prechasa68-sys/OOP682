from __future__ import annotations

from dataclasses import dataclass

import pygame

from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.base import CircleCollider, Entity


@dataclass
class EnemySpec:
    max_hp: int
    speed: float
    radius: float
    xp_drop: int
    color: tuple[int, int, int]


class Enemy(Entity):
    def __init__(self, pos: Vec2, spec: EnemySpec):
        super().__init__(pos=pos, collider=CircleCollider(radius=spec.radius))
        self.spec = spec
        self.hp = spec.max_hp
        self.dropped = False

    def steer_towards(self, target: Vec2, dt: float) -> None:
        direction = (target - self.pos).normalized()
        self.pos = self.pos + (direction * (self.spec.speed * dt))

    def damage(self, amount: int) -> None:
        self.hp -= int(amount)
        if self.hp <= 0:
            self.alive = False

    def draw(self, screen: pygame.Surface, camera: Vec2) -> None:
        p = self.pos - camera
        # Robber: dark body + bandana
        cx, cy = int(p.x), int(p.y)
        r = int(self.collider.radius)

        body = pygame.Rect(cx - r, cy - r + 2, r * 2, r * 2)
        pygame.draw.ellipse(screen, (35, 35, 42), body)

        # bandana
        band = pygame.Rect(cx - r + 2, cy - 4, r * 2 - 4, 7)
        pygame.draw.rect(screen, (165, 55, 55), band, border_radius=3)

        # small "mask" eye line
        pygame.draw.line(screen, (235, 235, 240), (cx - r // 2, cy - 1), (cx + r // 2, cy - 1), 2)

        pygame.draw.ellipse(screen, (0, 0, 0), body, 2)

