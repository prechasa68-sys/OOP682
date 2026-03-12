from __future__ import annotations

from dataclasses import dataclass
from math import hypot


@dataclass
class Vec2:
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * float(scalar), self.y * float(scalar))

    def length(self) -> float:
        return hypot(self.x, self.y)

    def normalized(self) -> "Vec2":
        l = self.length()
        if l <= 1e-9:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / l, self.y / l)

