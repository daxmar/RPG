from __future__ import annotations

try:
    import pygame
except Exception:  # pragma: no cover
    pygame = None


class CombatLog:
    """
    Log combat sederhana (menampilkan beberapa baris terakhir).

    Aman digunakan dalam proyek ini karena hanya dipakai jika pygame tersedia.
    """

    def __init__(self, screen, font_name: str | None = None, max_lines: int = 10):
        if pygame is None:  # pragma: no cover
            raise RuntimeError("pygame is not available")

        self.screen = screen
        self.font = pygame.font.SysFont(font_name, 16)
        self.max_lines = max_lines

    def draw(self, lines: list[str]) -> None:
        if pygame is None:  # pragma: no cover
            return

        visible = lines[-self.max_lines :]
        # tampilkan di sisi bawah
        x = 10
        y = self.screen.get_height() - 16 * (len(visible) + 1) - 10

        # header
        header = self.font.render("Combat Log", True, (180, 180, 255))
        self.screen.blit(header, (x, y - 18))

        for i, line in enumerate(visible):
            surf = self.font.render(line, True, (230, 230, 230))
            self.screen.blit(surf, (x, y + i * 16))
