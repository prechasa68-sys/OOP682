from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from reo_survivors.core.time import Cooldown
from reo_survivors.entities.projectile import Projectile

if TYPE_CHECKING:
    from reo_survivors.entities.enemy import Enemy
    from reo_survivors.entities.player import Player


@dataclass
class WeaponContext:
    player: Player
    nearest_enemy: Optional[Enemy]


class Weapon(ABC):
    """Strategy Pattern: each weapon implements its own firing behavior."""

    def __init__(self, name: str, base_cooldown: float):
        self.name = name
        self.base_cooldown = float(base_cooldown)
        self.cooldown = Cooldown(self.base_cooldown)
        self.level = 1

    def upgrade(self) -> None:
        self.level += 1

    def update(self, dt: float) -> None:
        self.cooldown.tick(dt)

    @abstractmethod
    def try_fire(self, ctx: WeaponContext) -> list[Projectile]:
        raise NotImplementedError

