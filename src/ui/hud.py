from __future__ import annotations

from dataclasses import dataclass

try:
    import pygame
except Exception:  # pragma: no cover
    pygame = None


@dataclass
class HudState:
    show_turn: bool = True


class HUD:
    """
    Minimal HUD untuk menampilkan HP Player/Enemy dan info turn.

    Tetap aman dipakai walau pygame tidak tersedia (akan gagal saat dipanggil).
    """

    def __init__(self, screen, font_name: str | None = None, hud_state: HudState | None = None):
        if pygame is None:  # pragma: no cover
            raise RuntimeError("pygame is not available")

        self.screen = screen
        self.font = pygame.font.SysFont(font_name, 18)
        self.hud_state = hud_state or HudState()

    def draw(self, lines: list[str]) -> None:
        if pygame is None:  # pragma: no cover
            return

        x, y = 10, 10
        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (230, 230, 230))
            self.screen.blit(surf, (x, y + i * 18))
