from __future__ import annotations

from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.base import Entity
from reo_survivors.entities.enemy import Enemy
from reo_survivors.entities.gem import Gem
from reo_survivors.entities.player import Player
from reo_survivors.entities.projectile import Projectile


def circles_overlap(a_pos: Vec2, a_r: float, b_pos: Vec2, b_r: float) -> bool:
    d = a_pos - b_pos
    rr = a_r + b_r
    return (d.x * d.x + d.y * d.y) <= (rr * rr)


class CollisionSystem:
    """Single-responsibility system: resolve hits/pickups."""

    def projectiles_vs_enemies(self, projectiles: list[Projectile], enemies: list[Enemy]) -> int:
        kills = 0
        for p in projectiles:
            if not p.alive:
                continue
            for e in enemies:
                if not e.alive:
                    continue
                if circles_overlap(p.pos, p.collider.radius, e.pos, e.collider.radius):
                    e.damage(p.damage)
                    p.alive = False
                    if not e.alive:
                        kills += 1
                    break
        return kills

    def player_vs_enemies(self, player: Player, enemies: list[Enemy], dt: float) -> int:
        """Return damage dealt to player (simple contact damage)."""
        damage = 0
        for e in enemies:
            if not e.alive:
                continue
            if circles_overlap(player.pos, player.collider.radius, e.pos, e.collider.radius):
                damage += int(15 * dt) + 1
        return damage

    def player_pickups(self, player: Player, gems: list[Gem]) -> int:
        xp = 0
        for g in gems:
            if not g.alive:
                continue
            if circles_overlap(player.pos, player.collider.radius + 8, g.pos, g.collider.radius):
                xp += g.xp
                g.alive = False
        return xp

