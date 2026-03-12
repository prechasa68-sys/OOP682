from __future__ import annotations

from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.projectile import Projectile
from reo_survivors.weapons.base import Weapon, WeaponContext


class Knife(Weapon):
    def __init__(self):
        super().__init__(name="Knife", base_cooldown=0.45)

    def try_fire(self, ctx: WeaponContext) -> list[Projectile]:
        if not self.cooldown.consume():
            return []
        player = ctx.player
        direction = player.facing.normalized()
        if direction.length() <= 0:
            direction = Vec2(1.0, 0.0)
        speed = 520.0 * player.stats.projectile_speed_mult
        damage = int(7 * player.stats.damage_mult)
        return [Projectile(pos=Vec2(player.pos.x, player.pos.y), vel=direction * speed, damage=damage)]

