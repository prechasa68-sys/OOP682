from __future__ import annotations

import random

import pygame

from reo_survivors.config import GameConfig
from reo_survivors.states.base import GameState
from reo_survivors.states.play import PlayState


class MenuState(GameState):
    def __init__(self, config: GameConfig):
        super().__init__()
        self.config = config
        pygame.font.init()
        self.font_title = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_hint = pygame.font.SysFont("consolas", 22)
        self.font_small = pygame.font.SysFont("consolas", 16)

        self._t = 0.0
        self._rng = random.Random(1337)
        self._particles: list[dict[str, float]] = []
        for _ in range(70):
            self._particles.append(self._new_particle(initial=True))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.next_state = PlayState(config=self.config)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.next_state = PlayState(config=self.config)

    def update(self, dt: float) -> None:
        self._t += dt
        for p in self._particles:
            p["y"] += p["vy"] * dt
            p["x"] += p["vx"] * dt
            p["rot"] += p["vr"] * dt
            if p["y"] > self.config.height + 40:
                p.update(self._new_particle(initial=False))

    def draw(self, screen: pygame.Surface) -> None:
        self._draw_gradient(screen)
        self._draw_particles(screen)

        # Title with shadow
        title_shadow = self.font_title.render("REO Survivors", True, (0, 0, 0))
        title = self.font_title.render("REO Survivors", True, (245, 250, 255))
        cx = self.config.width // 2
        screen.blit(title_shadow, title_shadow.get_rect(center=(cx + 3, 130 + 3)))
        screen.blit(title, title.get_rect(center=(cx, 130)))

        subtitle = self.font_small.render("Roguelike Survival • Soldier vs Robbers • Forest Map", True, (220, 235, 220))
        screen.blit(subtitle, subtitle.get_rect(center=(cx, 175)))

        # Start button panel
        panel = pygame.Rect(0, 0, 520, 120)
        panel.center = (cx, 300)
        pygame.draw.rect(screen, (18, 22, 26), panel, border_radius=16)
        pygame.draw.rect(screen, (120, 220, 160), panel, width=2, border_radius=16)

        hint1 = self.font_hint.render("Press ENTER to start", True, (240, 240, 240))
        hint2 = self.font_small.render("or click anywhere", True, (185, 205, 190))
        screen.blit(hint1, hint1.get_rect(center=(cx, 285)))
        screen.blit(hint2, hint2.get_rect(center=(cx, 322)))

        controls = self.font_small.render("Move: WASD/Arrows   Pause: ESC   Upgrade: 1/2/3, ↑↓ + Enter, Click", True, (200, 215, 205))
        screen.blit(controls, controls.get_rect(center=(cx, 500)))

    def _draw_gradient(self, screen: pygame.Surface) -> None:
        w, h = screen.get_size()
        top = pygame.Color(20, 60, 35)
        mid = pygame.Color(16, 32, 26)
        bot = pygame.Color(10, 10, 14)
        for y in range(h):
            t = y / max(1, h - 1)
            if t < 0.55:
                k = t / 0.55
                c = top.lerp(mid, k)
            else:
                k = (t - 0.55) / 0.45
                c = mid.lerp(bot, k)
            pygame.draw.line(screen, c, (0, y), (w, y))

        # Soft vignette
        vignette = pygame.Surface((w, h), pygame.SRCALPHA)
        vignette.fill((0, 0, 0, 0))
        pygame.draw.rect(vignette, (0, 0, 0, 110), vignette.get_rect(), width=40, border_radius=20)
        screen.blit(vignette, (0, 0))

    def _new_particle(self, initial: bool) -> dict[str, float]:
        w, h = self.config.width, self.config.height
        x = self._rng.uniform(0, w)
        y = self._rng.uniform(-40, h) if initial else self._rng.uniform(-120, -20)
        vy = self._rng.uniform(25, 95)
        vx = self._rng.uniform(-18, 18)
        size = self._rng.uniform(2.0, 5.5)
        rot = self._rng.uniform(0.0, 6.28)
        vr = self._rng.uniform(-1.6, 1.6)
        hue = self._rng.random()
        # leaf-like colors: green/yellow + occasional pink flower petal
        if hue < 0.80:
            col = (90, 210, 130, 170)
        elif hue < 0.95:
            col = (230, 230, 150, 170)
        else:
            col = (240, 150, 200, 170)
        return {"x": x, "y": y, "vx": vx, "vy": vy, "size": size, "rot": rot, "vr": vr, "r": col[0], "g": col[1], "b": col[2], "a": col[3]}

    def _draw_particles(self, screen: pygame.Surface) -> None:
        for p in self._particles:
            x = int(p["x"])
            y = int(p["y"])
            s = int(p["size"])
            col = (int(p["r"]), int(p["g"]), int(p["b"]), int(p["a"]))
            # simple "leaf" diamond
            pts = [(x, y - s), (x + s, y), (x, y + s), (x - s, y)]
            pygame.draw.polygon(screen, col, pts)

