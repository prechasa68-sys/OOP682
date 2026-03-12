from __future__ import annotations

from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.projectile import Projectile
from reo_survivors.weapons.base import Weapon, WeaponContext


class MagicWand(Weapon):
    def __init__(self):
        # Faster fire rate to feel like a gun for the soldier starter weapon.
        super().__init__(name="Magic Wand", base_cooldown=0.40)

    def try_fire(self, ctx: WeaponContext) -> list[Projectile]:
        if ctx.nearest_enemy is None:
            return []
        if not self.cooldown.consume():
            return []

        player = ctx.player
        direction = (ctx.nearest_enemy.pos - player.pos).normalized()
        speed = 420.0 * player.stats.projectile_speed_mult
        damage = int(10 * player.stats.damage_mult)
        return [Projectile(pos=Vec2(player.pos.x, player.pos.y), vel=direction * speed, damage=damage)]

