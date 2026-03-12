from __future__ import annotations

import sys

import pygame

from reo_survivors.config import GameConfig
from reo_survivors.states.menu import MenuState


class GameApp:
    def __init__(self, config: GameConfig):
        self.config = config
        pygame.init()
        pygame.display.set_caption(self.config.title)

        self.screen = pygame.display.set_mode((self.config.width, self.config.height))
        self.clock = pygame.time.Clock()
        self.state = MenuState(config=self.config)

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(self.config.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                self.state.handle_event(event)

            self.state.update(dt)
            if self.state.next_state is not None:
                self.state = self.state.next_state

            self.state.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


def main() -> None:
    config = GameConfig()
    app = GameApp(config)
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

