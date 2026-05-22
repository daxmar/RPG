from __future__ import annotations

import time

from src.entities.entity_manager import EntityManager
from src.entities.systems.combat_system import CombatManager
from src.worlds.data_loader import load_monsters


class StateManager:
    def __init__(self):
        self.entity_manager = EntityManager()
        self.state = "menu"

        self.combat: CombatManager | None = None

        self._frame_delay = 1.0  # untuk headless logging

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
        self.entity_manager.add_component(player, Health(hp=60, max_hp=60))
        self.entity_manager.add_component(
            player,
            Stats(
                strength=10,
                defense=5,
                agility=7,
                crit_chance=0.15,
                crit_multiplier=2.0,
            ),
        )

        enemy = self.entity_manager.create_entity("Enemy")
        self.entity_manager.add_component(
            enemy,
            Health(hp=enemy_data["max_hp"], max_hp=enemy_data["max_hp"]),
        )
        self.entity_manager.add_component(
            enemy,
            Stats(
                strength=enemy_data["strength"],
                defense=enemy_data["defense"],
                agility=enemy_data["agility"],
                crit_chance=enemy_data.get("crit_chance", 0.1),
                crit_multiplier=enemy_data.get("crit_multiplier", 1.5),
            ),
        )

        self.combat = CombatManager(
            entity_manager=self.entity_manager,
            players=[player],
            enemies=[enemy],
        )

    def run(self):
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

