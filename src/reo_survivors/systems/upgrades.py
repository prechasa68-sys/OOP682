from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, List, Protocol

from reo_survivors.entities.player import Player
from reo_survivors.weapons.knife import Knife
from reo_survivors.weapons.magic_wand import MagicWand


class Upgrade(Protocol):
    name: str
    description: str

    def apply(self, player: Player) -> None: ...


@dataclass(frozen=True)
class SimpleUpgrade:
    name: str
    description: str
    _apply: Callable[[Player], None]

    def apply(self, player: Player) -> None:
        self._apply(player)


class UpgradePool:
    """Open/Closed: add new upgrades by registering here."""

    def __init__(self) -> None:
        self._upgrades: List[Upgrade] = []
        self._register_defaults()

    def _register_defaults(self) -> None:
        self._upgrades.extend(
            [
                SimpleUpgrade(
                    name="Move Speed +10%",
                    description="Run faster.",
                    _apply=lambda p: setattr(p.stats, "speed", p.stats.speed * 1.10),
                ),
                SimpleUpgrade(
                    name="Damage +15%",
                    description="All weapons deal more damage.",
                    _apply=lambda p: setattr(p.stats, "damage_mult", p.stats.damage_mult * 1.15),
                ),
                SimpleUpgrade(
                    name="Cooldown -10%",
                    description="Weapons fire more often.",
                    _apply=lambda p: setattr(p.stats, "cooldown_mult", p.stats.cooldown_mult * 0.90),
                ),
                SimpleUpgrade(
                    name="Projectile Speed +15%",
                    description="Projectiles travel faster.",
                    _apply=lambda p: setattr(
                        p.stats, "projectile_speed_mult", p.stats.projectile_speed_mult * 1.15
                    ),
                ),
                SimpleUpgrade(
                    name="Gain Magic Wand",
                    description="Adds a targeting weapon.",
                    _apply=self._give_magic_wand,
                ),
                SimpleUpgrade(
                    name="Gain Knife",
                    description="Fires in your facing direction.",
                    _apply=self._give_knife,
                ),
            ]
        )

    @staticmethod
    def _give_magic_wand(player: Player) -> None:
        if any(w.name == "Magic Wand" for w in player.weapons):
            # If already has it, upgrade its level instead.
            for w in player.weapons:
                if w.name == "Magic Wand":
                    w.upgrade()
                    return
        player.weapons.append(MagicWand())

    @staticmethod
    def _give_knife(player: Player) -> None:
        if any(w.name == "Knife" for w in player.weapons):
            for w in player.weapons:
                if w.name == "Knife":
                    w.upgrade()
                    return
        player.weapons.append(Knife())

    def roll(self, k: int = 3) -> list[Upgrade]:
        if len(self._upgrades) <= k:
            return list(self._upgrades)
        return random.sample(self._upgrades, k=k)

    def give_starter_loadout(self, player: Player) -> None:
        """Convenience for demo/game start (keeps PlayState simpler)."""
        self._give_magic_wand(player)

