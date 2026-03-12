from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import pygame


class GameState(ABC):
    """State Pattern: all screens share this interface."""

    def __init__(self) -> None:
        self.next_state: Optional["GameState"] = None

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError

