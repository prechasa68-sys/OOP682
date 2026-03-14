from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    title: str = "REO Survivors"
    width: int = 960
    height: int = 540
    fps: int = 60

    # World tuning
    player_speed: float = 220.0
    enemy_base_speed: float = 90.0

    # Spawning
    spawn_radius: float = 520.0
    spawn_rate_start: float = 0.45  # enemies / sec
    spawn_rate_growth: float = 0.008  # per sec
    max_enemies: int = 65

    # XP/level
    base_xp_to_level: int = 20
    xp_growth: float = 1.35  # Each level requires 35% more XP than previous

    # Win condition
    win_time_seconds: float = 60.0  # survive for N seconds to win
