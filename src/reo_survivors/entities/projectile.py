from __future__ import annotations

import pygame

from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.base import CircleCollider, Entity


class Projectile(Entity):
    def __init__(self, pos: Vec2, vel: Vec2, damage: int, lifetime: float = 2.0):
        super().__init__(pos=pos, collider=CircleCollider(radius=6))
        self.vel = vel
        self.damage = int(damage)
        self._life = float(lifetime)

    def update(self, dt: float) -> None:
        self.pos = self.pos + (self.vel * dt)
        self._life -= dt
        if self._life <= 0:
            self.alive = False

    def draw(self, screen: pygame.Surface, camera: Vec2) -> None:
        p = self.pos - camera
        pygame.draw.circle(screen, (255, 240, 120), (int(p.x), int(p.y)), int(self.collider.radius))

