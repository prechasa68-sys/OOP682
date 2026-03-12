from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List

import pygame

from reo_survivors.config import GameConfig
from reo_survivors.core.events import EventBus, PlayerLeveledUp
from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.base import CircleCollider, Entity
if TYPE_CHECKING:
    from reo_survivors.weapons.base import Weapon


@dataclass
class Stats:
    speed: float
    damage_mult: float = 1.0
    cooldown_mult: float = 1.0
    projectile_speed_mult: float = 1.0


class Health:
    def __init__(self, max_hp: int):
        self._max = int(max_hp)
        self._hp = int(max_hp)

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def max_hp(self) -> int:
        return self._max

    def heal_full(self) -> None:
        self._hp = self._max

    def damage(self, amount: int) -> None:
        self._hp = max(0, self._hp - int(amount))

    def dead(self) -> bool:
        return self._hp <= 0


class Player(Entity):
    def __init__(self, config: GameConfig, event_bus: EventBus):
        super().__init__(pos=Vec2(0.0, 0.0), collider=CircleCollider(radius=16))
        self.config = config
        self.event_bus = event_bus

        self.stats = Stats(speed=config.player_speed)
        self.health = Health(max_hp=100)

        self.level = 1
        self.xp = 0
        self.xp_to_next = config.base_xp_to_level

        self.weapons: List[Weapon] = []
        self._move_dir = Vec2(0.0, 0.0)
        self._facing = Vec2(1.0, 0.0)

    @property
    def facing(self) -> Vec2:
        return self._facing

    def add_xp(self, amount: int) -> bool:
        self.xp += int(amount)
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * self.config.xp_growth) + 1
            self.event_bus.publish(PlayerLeveledUp(new_level=self.level))
            leveled = True
        return leveled

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        x = 0.0
        y = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x -= 1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x += 1.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y -= 1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y += 1.0

        self._move_dir = Vec2(x, y).normalized()
        if self._move_dir.length() > 0:
            self._facing = self._move_dir

    def update(self, dt: float) -> None:
        self.pos = self.pos + (self._move_dir * (self.stats.speed * dt))

    def draw(self, screen: pygame.Surface, camera: Vec2) -> None:
        p = self.pos - camera
        # Soldier (top-down): body + helmet + gun barrel facing direction
        cx, cy = int(p.x), int(p.y)

        # shadow
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy + 10), 14, 0)

        # body
        body = pygame.Rect(cx - 12, cy - 10, 24, 24)
        pygame.draw.rect(screen, (60, 120, 75), body, border_radius=6)

        # helmet
        pygame.draw.circle(screen, (75, 90, 75), (cx, cy - 12), 10)
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy - 12), 10, 1)

        # gun
        f = self.facing.normalized()
        gx1, gy1 = cx + int(f.x * 8), cy + int(f.y * 8)
        gx2, gy2 = cx + int(f.x * 18), cy + int(f.y * 18)
        pygame.draw.line(screen, (30, 30, 35), (gx1, gy1), (gx2, gy2), 5)
        pygame.draw.line(screen, (0, 0, 0), (gx1, gy1), (gx2, gy2), 1)

        # outline
        pygame.draw.rect(screen, (0, 0, 0), body, width=2, border_radius=6)

