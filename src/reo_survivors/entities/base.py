from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pygame

from reo_survivors.core.math2d import Vec2


class Updatable(Protocol):
    def update(self, dt: float) -> None: ...


class Drawable(Protocol):
    def draw(self, screen: pygame.Surface, camera: Vec2) -> None: ...


@dataclass
class CircleCollider:
    radius: float


class Entity:
    """Base class for world objects (Inheritance + Polymorphism)."""

    def __init__(self, pos: Vec2, collider: CircleCollider):
        self.pos = pos
        self.collider = collider
        self.alive = True

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface, camera: Vec2) -> None:
        raise NotImplementedError

