from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, List, Type


class Event:
    pass


@dataclass(frozen=True)
class EnemyKilled(Event):
    xp: int


@dataclass(frozen=True)
class PlayerDamaged(Event):
    amount: int


@dataclass(frozen=True)
class PlayerLeveledUp(Event):
    new_level: int


Handler = Callable[[Event], None]


class EventBus:
    """Observer / Pub-Sub. Keeps gameplay decoupled (SOLID - DIP)."""

    def __init__(self) -> None:
        self._handlers: DefaultDict[Type[Event], List[Handler]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        for handler in list(self._handlers[type(event)]):
            handler(event)

