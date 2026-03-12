from __future__ import annotations

import math
import random
from dataclasses import dataclass

from reo_survivors.config import GameConfig
from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.enemy import Enemy, EnemySpec


class EnemyFactory:
    """Factory Pattern: create enemy variants based on difficulty/time."""

    def __init__(self, config: GameConfig):
        self.config = config

    def create(self, difficulty: float, pos: Vec2) -> Enemy:
        # Difficulty ~ seconds elapsed. Keep it simple but scalable.
        tier = 1 + int(difficulty // 25)
        hp = 18 + (tier * 6)
        speed = self.config.enemy_base_speed + (tier * 10)
        radius = 14 + min(8, tier * 2)
        xp = 1 + min(5, tier)
        color = (220, 90, 90) if tier <= 2 else (240, 130, 70)
        return Enemy(pos=pos, spec=EnemySpec(max_hp=hp, speed=speed, radius=radius, xp_drop=xp, color=color))


@dataclass
class SpawnResult:
    enemies: list[Enemy]


class EnemySpawner:
    """SRP: spawn enemies around player with increasing rate."""

    def __init__(self, config: GameConfig, factory: EnemyFactory):
        self.config = config
        self.factory = factory
        self._t = 0.0
        self._accum = 0.0

    def update(self, dt: float, player_pos: Vec2, current_enemy_count: int) -> SpawnResult:
        self._t += dt
        rate = self.config.spawn_rate_start + self.config.spawn_rate_growth * self._t
        self._accum += rate * dt

        spawned: list[Enemy] = []
        while self._accum >= 1.0:
            if current_enemy_count + len(spawned) >= self.config.max_enemies:
                # Stop accumulating too much spawn debt when capped.
                self._accum = 0.0
                break
            self._accum -= 1.0
            spawned.append(self._spawn_one(player_pos, difficulty=self._t))
        return SpawnResult(enemies=spawned)

    def _spawn_one(self, player_pos: Vec2, difficulty: float) -> Enemy:
        ang = random.random() * 6.283185307
        r = self.config.spawn_radius
        jitter = random.uniform(0.85, 1.05)
        pos = Vec2(
            player_pos.x + r * jitter * math.cos(ang),
            player_pos.y + r * jitter * math.sin(ang),
        )
        return self.factory.create(difficulty=difficulty, pos=pos)

