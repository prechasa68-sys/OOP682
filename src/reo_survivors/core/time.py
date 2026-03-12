from __future__ import annotations


class Cooldown:
    """Small utility class for cooldown timers (encapsulated state)."""

    def __init__(self, seconds: float):
        self._period = float(seconds)
        self._t = 0.0

    def set_period(self, seconds: float) -> None:
        self._period = max(0.0, float(seconds))

    def reset(self) -> None:
        self._t = 0.0

    def tick(self, dt: float) -> None:
        self._t += float(dt)

    def ready(self) -> bool:
        return self._t >= self._period

    def consume(self) -> bool:
        """Return True if ready, and consume the cooldown."""
        if not self.ready():
            return False
        self._t = 0.0
        return True

