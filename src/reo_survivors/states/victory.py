from __future__ import annotations

import pygame

from reo_survivors.config import GameConfig
from reo_survivors.states.base import GameState


class VictoryState(GameState):
    def __init__(self, config: GameConfig, kills: int, time_survived: float):
        super().__init__()
        self.config = config
        self.kills = kills
        self.time_survived = time_survived
        pygame.font.init()
        self.font_big = pygame.font.SysFont("consolas", 40, bold=True)
        self.font = pygame.font.SysFont("consolas", 20)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Lazy import to avoid circular imports.
            from reo_survivors.states.menu import MenuState

            self.next_state = MenuState(config=self.config)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((10, 14, 10))
        title = self.font_big.render("VICTORY!", True, (240, 255, 240))
        stats = self.font.render(
            f"Kills: {self.kills}   Time: {self.time_survived:.1f}s", True, (200, 220, 200)
        )
        hint = self.font.render("Press ENTER to return to menu", True, (170, 190, 170))

        screen.blit(title, title.get_rect(center=(self.config.width // 2, 180)))
        screen.blit(stats, stats.get_rect(center=(self.config.width // 2, 260)))
        screen.blit(hint, hint.get_rect(center=(self.config.width // 2, 320)))

