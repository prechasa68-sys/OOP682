from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from reo_survivors.core.math2d import Vec2


@dataclass(frozen=True)
class MapPalette:
    # Forest palette
    grass1: tuple[int, int, int] = (34, 60, 34)
    grass2: tuple[int, int, int] = (30, 54, 30)
    dirt1: tuple[int, int, int] = (92, 78, 56)
    dirt2: tuple[int, int, int] = (84, 70, 52)
    rock: tuple[int, int, int] = (100, 106, 116)
    tree: tuple[int, int, int] = (18, 90, 38)
    tree_dark: tuple[int, int, int] = (14, 72, 30)
    bush: tuple[int, int, int] = (22, 110, 44)
    bush_dark: tuple[int, int, int] = (16, 92, 36)
    flower_pink: tuple[int, int, int] = (235, 140, 190)
    flower_yellow: tuple[int, int, int] = (245, 235, 150)


class TileMap:
    """
    Lightweight procedural tile map (no external assets).
    Renders a 'wide' world with grass + winding paths + decorations.
    """

    def __init__(self, tile_size: int = 48, seed: int = 1337, palette: MapPalette | None = None):
        self.tile_size = int(tile_size)
        self.seed = int(seed)
        self.palette = palette or MapPalette()

    def draw(self, screen: pygame.Surface, camera: Vec2) -> None:
        w, h = screen.get_size()
        ts = self.tile_size

        # Compute visible tile range in world coordinates
        left = int(math.floor(camera.x / ts)) - 1
        top = int(math.floor(camera.y / ts)) - 1
        right = int(math.floor((camera.x + w) / ts)) + 1
        bottom = int(math.floor((camera.y + h) / ts)) + 1

        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                self._draw_tile(screen, tx, ty, camera)

    def _draw_tile(self, screen: pygame.Surface, tx: int, ty: int, camera: Vec2) -> None:
        ts = self.tile_size
        x = tx * ts - camera.x
        y = ty * ts - camera.y
        rect = pygame.Rect(int(x), int(y), ts, ts)

        # Base grass variation
        g = self.palette.grass1 if (self._hash(tx, ty) & 1) == 0 else self.palette.grass2
        pygame.draw.rect(screen, g, rect)

        # Dirt trails: use a simple deterministic "noise" field to carve paths.
        n = self._noise(tx, ty)
        on_path = (0.46 < n < 0.54) or (0.71 < n < 0.745)
        if on_path:
            c = self.palette.dirt1 if (self._hash(tx + 9, ty - 3) & 1) == 0 else self.palette.dirt2
            pygame.draw.rect(screen, c, rect)
            # subtle texture dots
            self._draw_dirt_specks(screen, rect, tx, ty)
            return

        # Decorations (trees/bushes/rocks/flowers)
        deco_roll = self._hash(tx * 7, ty * 11) % 100
        if deco_roll < 4:
            self._draw_tree(screen, rect, tx, ty)
        elif 4 <= deco_roll < 8:
            self._draw_bush(screen, rect, tx, ty)
        elif 8 <= deco_roll < 10:
            self._draw_rock(screen, rect, tx, ty)
        else:
            self._draw_flowers(screen, rect, tx, ty)

        # No grid: keep it natural for a forest.

    def _draw_tree(self, screen: pygame.Surface, rect: pygame.Rect, tx: int, ty: int) -> None:
        # trunk
        trunk = pygame.Rect(rect.centerx - 3, rect.centery + 6, 6, 12)
        pygame.draw.rect(screen, (80, 55, 30), trunk)
        # canopy
        base = self.palette.tree if (self._hash(tx + 2, ty + 2) & 1) == 0 else self.palette.tree_dark
        pygame.draw.circle(screen, base, (rect.centerx, rect.centery + 2), 14)
        pygame.draw.circle(screen, (0, 0, 0), (rect.centerx, rect.centery + 2), 14, 1)

    def _draw_bush(self, screen: pygame.Surface, rect: pygame.Rect, tx: int, ty: int) -> None:
        base = self.palette.bush if (self._hash(tx + 5, ty - 4) & 1) == 0 else self.palette.bush_dark
        cx, cy = rect.centerx, rect.centery + 6
        pygame.draw.circle(screen, base, (cx - 8, cy), 10)
        pygame.draw.circle(screen, base, (cx + 6, cy + 2), 9)
        pygame.draw.circle(screen, base, (cx, cy - 6), 9)
        pygame.draw.circle(screen, (0, 0, 0), (cx - 8, cy), 10, 1)
        pygame.draw.circle(screen, (0, 0, 0), (cx + 6, cy + 2), 9, 1)
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy - 6), 9, 1)

    def _draw_rock(self, screen: pygame.Surface, rect: pygame.Rect, tx: int, ty: int) -> None:
        c = self.palette.rock
        r = pygame.Rect(rect.centerx - 10, rect.centery + 4, 20, 14)
        pygame.draw.ellipse(screen, c, r)
        pygame.draw.ellipse(screen, (0, 0, 0), r, 1)

    def _draw_flowers(self, screen: pygame.Surface, rect: pygame.Rect, tx: int, ty: int) -> None:
        # Scatter 0-3 tiny flowers on some tiles
        roll = self._hash(tx + 19, ty - 23) % 100
        if roll > 16:
            return
        count = 1 + (self._hash(tx - 7, ty + 11) % 3)
        for i in range(count):
            hx = self._hash(tx * 31 + i * 3, ty * 17 - i * 5)
            fx = rect.x + 10 + (hx % (rect.w - 20))
            fy = rect.y + 12 + ((hx >> 8) % (rect.h - 24))
            col = self.palette.flower_pink if (hx & 1) == 0 else self.palette.flower_yellow
            pygame.draw.circle(screen, col, (fx, fy), 2)
            pygame.draw.circle(screen, (0, 0, 0), (fx, fy), 2, 1)

    def _draw_dirt_specks(self, screen: pygame.Surface, rect: pygame.Rect, tx: int, ty: int) -> None:
        # Small stones/specks for texture
        for i in range(3):
            h = self._hash(tx + i * 13, ty - i * 9)
            sx = rect.x + 6 + (h % (rect.w - 12))
            sy = rect.y + 6 + ((h >> 8) % (rect.h - 12))
            pygame.draw.circle(screen, (70, 62, 48), (sx, sy), 1)

    def _hash(self, a: int, b: int) -> int:
        # Deterministic hash, stable across runs
        x = (a * 374761393 + b * 668265263 + self.seed * 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        x = (x ^ (x >> 13)) * 1274126177 & 0xFFFFFFFFFFFFFFFF
        return int(x ^ (x >> 16))

    def _noise(self, tx: int, ty: int) -> float:
        # Convert hash to [0,1)
        return (self._hash(tx, ty) & 0xFFFF) / 65536.0

