from __future__ import annotations

import time

from src.entities.entity_manager import EntityManager
from src.entities.systems.combat_system import CombatManager
from src.worlds.data_loader import load_monsters

try:
    import pygame
except Exception:  # pragma: no cover
    pygame = None


class StateManager:
    def __init__(self):
        self.entity_manager = EntityManager()
        self.state = "menu"

        self.combat: CombatManager | None = None

        # untuk headless logging / pacing
        self._frame_delay = 1.0

        # untuk pygame
        self._turn_interval_sec = 1.0
        self._last_turn_at = 0.0

        # headless fallback
        self._use_pygame = pygame is not None

        # pygame UI objects (dibuat sekali dan di-reuse)
        self._hud = None
        self._combat_log_ui = None

    def _setup_combat(self):
        # Buat 1 player dan 1 enemy dari data
        monsters = load_monsters()
        enemy_data = monsters[0] if monsters else {
            "name": "Slime",
            "max_hp": 35,
            "strength": 6,
            "defense": 2,
            "agility": 4,
            "crit_chance": 0.1,
            "crit_multiplier": 1.5,
        }

        # Lazy import components (biar modul bisa dipakai tanpa pygame)
        from src.entities.components import Health, Stats

        player = self.entity_manager.create_entity("Player")
        self.entity_manager.add_component(player, Health(current=60, max=60))
        self.entity_manager.add_component(
            player,
            Stats(
                strength=10,
                defense=5,
                agility=7,
                critical_chance=0.15,
            ),
        )

        enemy = self.entity_manager.create_entity("Enemy")
        self.entity_manager.add_component(
            enemy,
            Health(current=enemy_data["max_hp"], max=enemy_data["max_hp"]),
        )
        self.entity_manager.add_component(
            enemy,
            Stats(
                strength=enemy_data["strength"],
                defense=enemy_data["defense"],
                agility=enemy_data["agility"],
                critical_chance=enemy_data.get("crit_chance", 0.1),
            ),
        )

        self.combat = CombatManager(
            entity_manager=self.entity_manager,
            players=[player],
            enemies=[enemy],
        )

    def _draw_headless_log(self):
        # keep behavior: combat_system sudah print per step
        pass

    def _draw_menu_pygame(self, screen, font) -> None:
        screen.fill((20, 20, 30))
        msg = "Aetheria RPG - Press any key to start combat"
        surf = font.render(msg, True, (230, 230, 230))
        screen.blit(surf, (20, 20))
        pygame.display.flip()

    def _draw_combat_pygame(self, screen) -> None:
        from src.entities.components import Health
        from src.ui.combat_log import CombatLog
        from src.ui.hud import HUD

        assert self.combat is not None

        # init UI sekali saat masuk ke pygame mode
        if self._hud is None or self._combat_log_ui is None:
            self._hud = HUD(screen)
            self._combat_log_ui = CombatLog(screen)

        player = self.combat.players[0]
        enemy = self.combat.enemies[0]
        p_hp: Health = self.entity_manager.get_component(player, Health)
        e_hp: Health = self.entity_manager.get_component(enemy, Health)

        lines = [
            f"Player HP: {p_hp.current}/{p_hp.max}",
            f"Enemy HP: {e_hp.current}/{e_hp.max}",
            f"Turn: {min(self.combat.turn_index + 1, 10**9)}",
        ]
        screen.fill((10, 10, 15))
        self._hud.draw(lines)
        self._combat_log_ui.draw(self.combat.log)

        pygame.display.flip()

    def run(self):
        if not self._use_pygame:
            # Mode minimal: headless demo berjalan otomatis.
            while self.state != "exit":
                if self.state == "menu":
                    self._setup_combat()
                    self.state = "combat"
                    continue

                if self.state == "combat":
                    assert self.combat is not None

                    done = self.combat.step()
                    time.sleep(self._frame_delay)

                    if done:
                        self.state = "exit"
                    continue

                raise RuntimeError(f"Unknown state: {self.state}")

        # pygame mode
        if pygame is None:  # pragma: no cover
            raise RuntimeError("pygame is not available but pygame mode was entered")

        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Aetheria RPG (Minimal)")

        font = pygame.font.SysFont(None, 22)
        clock = pygame.time.Clock()

        self._last_turn_at = time.time()

        while self.state != "exit":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "exit"

                if self.state == "menu" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    self._setup_combat()
                    self.state = "combat"
                    self._last_turn_at = time.time()

            if self.state == "menu":
                self._draw_menu_pygame(screen, font)
                clock.tick(60)
                continue

            if self.state == "combat":
                assert self.combat is not None

                now = time.time()
                if now - self._last_turn_at >= self._turn_interval_sec:
                    done = self.combat.step()
                    self._last_turn_at = now
                    if done:
                        self.state = "exit"

                self._draw_combat_pygame(screen)
                clock.tick(60)
                continue

            raise RuntimeError(f"Unknown state: {self.state}")

