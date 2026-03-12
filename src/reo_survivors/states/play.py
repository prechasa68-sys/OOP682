from __future__ import annotations

from dataclasses import dataclass

import pygame

from reo_survivors.config import GameConfig
from reo_survivors.core.events import EnemyKilled, EventBus, PlayerLeveledUp
from reo_survivors.core.math2d import Vec2
from reo_survivors.entities.enemy import Enemy
from reo_survivors.entities.gem import Gem
from reo_survivors.entities.player import Player
from reo_survivors.entities.projectile import Projectile
from reo_survivors.states.base import GameState
from reo_survivors.states.game_over import GameOverState
from reo_survivors.states.pause import PauseState
from reo_survivors.states.victory import VictoryState
from reo_survivors.systems.collision import CollisionSystem
from reo_survivors.systems.spawner import EnemyFactory, EnemySpawner
from reo_survivors.systems.upgrades import Upgrade, UpgradePool
from reo_survivors.weapons.base import WeaponContext
from reo_survivors.world.map import TileMap


@dataclass
class UpgradeChoice:
    options: list[Upgrade]
    selected: int = 0


class PlayState(GameState):
    def __init__(self, config: GameConfig):
        super().__init__()
        self.config = config
        pygame.font.init()

        self.event_bus = EventBus()
        self.player = Player(config=self.config, event_bus=self.event_bus)

        self.enemies: list[Enemy] = []
        self.projectiles: list[Projectile] = []
        self.gems: list[Gem] = []

        self.collision = CollisionSystem()
        self.spawner = EnemySpawner(config=self.config, factory=EnemyFactory(config=self.config))
        self.upgrades = UpgradePool()
        self.map = TileMap(tile_size=48, seed=1337)

        self.elapsed = 0.0
        self.score_kills = 0

        self.font_hud = pygame.font.SysFont("consolas", 18)
        self.font_big = pygame.font.SysFont("consolas", 28, bold=True)

        self.choice: UpgradeChoice | None = None
        self.event_bus.subscribe(PlayerLeveledUp, self._on_level_up)

        # Start with 1 weapon so demo feels active.
        self.upgrades.give_starter_loadout(self.player)

    def _on_level_up(self, event: PlayerLeveledUp) -> None:
        self.choice = UpgradeChoice(options=self.upgrades.roll(3), selected=0)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.choice is None:
                self.next_state = PauseState(config=self.config, play_state=self)
            return

        if self.choice is not None:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    self.choice.selected = 0
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    self.choice.selected = 1
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    self.choice.selected = 2
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.choice.selected = (self.choice.selected - 1) % len(self.choice.options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.choice.selected = (self.choice.selected + 1) % len(self.choice.options)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self._apply_selected_upgrade()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_upgrade_mouse(event.pos)

    def _apply_selected_upgrade(self) -> None:
        assert self.choice is not None
        idx = max(0, min(self.choice.selected, len(self.choice.options) - 1))
        self.choice.options[idx].apply(self.player)
        self.choice = None

    def _handle_upgrade_mouse(self, mouse_pos: tuple[int, int]) -> None:
        assert self.choice is not None
        mx, my = mouse_pos
        for i in range(len(self.choice.options)):
            y = 160 + i * 90
            box = pygame.Rect(self.config.width // 2 - 330, y - 30, 660, 70)
            if box.collidepoint(mx, my):
                self.choice.selected = i
                self._apply_selected_upgrade()
                return

    def update(self, dt: float) -> None:
        if self.choice is not None:
            # Freeze world while choosing upgrade.
            return

        self.elapsed += dt
        if self.elapsed >= self.config.win_time_seconds:
            self.next_state = VictoryState(
                config=self.config, kills=self.score_kills, time_survived=self.elapsed
            )
            return
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt)

        # Spawn enemies
        self.enemies.extend(
            self.spawner.update(dt, player_pos=self.player.pos, current_enemy_count=len(self.enemies)).enemies
        )

        # Enemies chase
        for e in self.enemies:
            if e.alive:
                e.steer_towards(self.player.pos, dt)

        # Weapons auto-fire
        nearest = self._nearest_enemy()
        ctx = WeaponContext(player=self.player, nearest_enemy=nearest)
        can_shoot = self._enemy_in_view_margin()
        for w in self.player.weapons:
            w.cooldown.set_period(w.base_cooldown * self.player.stats.cooldown_mult)
            w.update(dt)
            if can_shoot:
                self.projectiles.extend(w.try_fire(ctx))

        # Update projectiles
        for p in self.projectiles:
            if p.alive:
                p.update(dt)

        # Collisions
        self.collision.projectiles_vs_enemies(self.projectiles, self.enemies)
        dmg = self.collision.player_vs_enemies(self.player, self.enemies, dt)
        if dmg > 0:
            self.player.health.damage(dmg)

        # Drops
        for e in self.enemies:
            if (not e.alive) and (not e.dropped):
                e.dropped = True
                self.score_kills += 1
                self.gems.append(Gem(pos=Vec2(e.pos.x, e.pos.y), xp=e.spec.xp_drop))
                self.event_bus.publish(EnemyKilled(xp=e.spec.xp_drop))

        # Pickup XP
        gained = self.collision.player_pickups(self.player, self.gems)
        if gained:
            self.player.add_xp(gained)

        # Cleanup
        self.enemies = [e for e in self.enemies if e.alive or (not e.dropped)]
        self.projectiles = [p for p in self.projectiles if p.alive]
        self.gems = [g for g in self.gems if g.alive]

        if self.player.health.dead():
            self.next_state = GameOverState(config=self.config, kills=self.score_kills, time_survived=self.elapsed)

    def _nearest_enemy(self) -> Enemy | None:
        best: Enemy | None = None
        best_d2 = 1e30
        for e in self.enemies:
            if not e.alive:
                continue
            d = e.pos - self.player.pos
            d2 = d.x * d.x + d.y * d.y
            if d2 < best_d2:
                best_d2 = d2
                best = e
        return best

    def _enemy_in_view_margin(self, margin: int = 60) -> bool:
        """Start shooting only after at least one enemy has entered the screen (with margin)."""
        cam_x = self.player.pos.x - self.config.width / 2
        cam_y = self.player.pos.y - self.config.height / 2
        left = cam_x - margin
        top = cam_y - margin
        right = cam_x + self.config.width + margin
        bottom = cam_y + self.config.height + margin

        for e in self.enemies:
            if not e.alive:
                continue
            if left <= e.pos.x <= right and top <= e.pos.y <= bottom:
                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        camera = Vec2(self.player.pos.x - self.config.width / 2, self.player.pos.y - self.config.height / 2)
        self.map.draw(screen, camera)

        # Draw world
        for g in self.gems:
            g.draw(screen, camera)
        for e in self.enemies:
            if e.alive:
                e.draw(screen, camera)
        for p in self.projectiles:
            p.draw(screen, camera)
        self.player.draw(screen, camera)

        self._draw_hud(screen)
        if self.choice is not None:
            self._draw_upgrade_overlay(screen)

    def _draw_hud(self, screen: pygame.Surface) -> None:
        hp = self.player.health.hp
        max_hp = self.player.health.max_hp
        txt = f"HP {hp}/{max_hp} | LV {self.player.level} | XP {self.player.xp}/{self.player.xp_to_next} | Kills {self.score_kills}"
        surf = self.font_hud.render(txt, True, (230, 230, 240))
        screen.blit(surf, (12, 10))

    def _draw_upgrade_overlay(self, screen: pygame.Surface) -> None:
        assert self.choice is not None

        overlay = pygame.Surface((self.config.width, self.config.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.font_big.render("LEVEL UP! Choose an upgrade", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(self.config.width // 2, 90)))

        for i, up in enumerate(self.choice.options):
            y = 160 + i * 90
            selected = (i == self.choice.selected)
            color = (255, 255, 255) if selected else (210, 210, 220)
            box = pygame.Rect(self.config.width // 2 - 330, y - 30, 660, 70)
            pygame.draw.rect(screen, (40, 40, 52), box, border_radius=10)
            pygame.draw.rect(screen, (120, 220, 255) if selected else (90, 90, 110), box, width=2, border_radius=10)

            name = self.font_big.render(f"{i+1}. {up.name}", True, color)
            desc = self.font_hud.render(up.description, True, (190, 190, 200))
            screen.blit(name, (box.x + 18, box.y + 10))
            screen.blit(desc, (box.x + 18, box.y + 42))

