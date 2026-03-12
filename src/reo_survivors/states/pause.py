from __future__ import annotations

import pygame

from reo_survivors.config import GameConfig
from reo_survivors.states.base import GameState


class PauseState(GameState):
    def __init__(self, config: GameConfig, play_state: GameState):
        super().__init__()
        self.config = config
        self.play_state = play_state
        pygame.font.init()
        self.font_big = pygame.font.SysFont("consolas", 38, bold=True)
        self.font_hint = pygame.font.SysFont("consolas", 20)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = self.play_state

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # Draw underlying play scene (frozen)
        self.play_state.draw(screen)

        overlay = pygame.Surface((self.config.width, self.config.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        t = self.font_big.render("PAUSED", True, (255, 255, 255))
        h = self.font_hint.render("Press ESC to resume", True, (210, 210, 220))
        screen.blit(t, t.get_rect(center=(self.config.width // 2, self.config.height // 2 - 20)))
        screen.blit(h, h.get_rect(center=(self.config.width // 2, self.config.height // 2 + 30)))

