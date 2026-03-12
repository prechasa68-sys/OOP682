from __future__ import annotations

import pygame

from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.base import CircleCollider, Entity


class Gem(Entity):
    def __init__(self, pos: Vec2, xp: int):
        super().__init__(pos=pos, collider=CircleCollider(radius=10))
        self.xp = int(xp)

    def draw(self, screen: pygame.Surface, camera: Vec2) -> None:
        p = self.pos - camera
        pygame.draw.circle(screen, (120, 255, 160), (int(p.x), int(p.y)), int(self.collider.radius))

