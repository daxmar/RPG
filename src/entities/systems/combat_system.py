from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from src.entities.components import Health, Stats
from src.entities.entity_manager import Entity, EntityManager


# --- Command Pattern ---
class Command:
    def execute(self) -> None:  # pragma: no cover
        raise NotImplementedError

    def undo(self) -> None:  # pragma: no cover
        raise NotImplementedError


@dataclass
class AttackResult:
    attacker: Entity
    target: Entity
    damage: int
    critical: bool


class AttackCommand(Command):
    def __init__(
        self,
        entity_manager: EntityManager,
        attacker: Entity,
        target: Entity,
        rng: random.Random | None = None,
    ):
        self.entity_manager = entity_manager
        self.attacker = attacker
        self.target = target
        self.rng = rng or random.Random()

        self._prev_target_hp: int | None = None
        self.result: AttackResult | None = None

    def execute(self) -> AttackResult:
        target_health: Health = self.entity_manager.get_component(self.target, Health)
        attacker_stats: Stats = self.entity_manager.get_component(self.attacker, Stats)
        target_stats: Stats = self.entity_manager.get_component(self.target, Stats)

        self._prev_target_hp = target_health.hp

        base_damage = max(1, attacker_stats.strength - target_stats.defense)

        critical = self.rng.random() < attacker_stats.crit_chance
        damage = base_damage
        if critical:
            damage = int(damage * attacker_stats.crit_multiplier)

        target_health.hp = max(0, target_health.hp - damage)

        self.result = AttackResult(
            attacker=self.attacker,
            target=self.target,
            damage=damage,
            critical=critical,
        )
        return self.result

    def undo(self) -> None:
        if self._prev_target_hp is None:
            return
        target_health: Health = self.entity_manager.get_component(self.target, Health)
        target_health.hp = self._prev_target_hp


# --- Combat Manager ---
class CombatManager:
    def __init__(
        self,
        entity_manager: EntityManager,
        players: List[Entity],
        enemies: List[Entity],
    ):
        self.entity_manager = entity_manager
        self.players = players
        self.enemies = enemies

        self.turn_queue: List[Entity] = []
        self.turn_index = 0

        self.rng = random.Random(42)

        self.log: List[str] = []

        self._init_queue()

    def _init_queue(self):
        self.turn_queue = self.players + self.enemies
        # inisialisasi: agility tertinggi dulu
        self.turn_queue.sort(key=lambda e: self.entity_manager.get_component(e, Stats).agility, reverse=True)

    def _living(self, entities: List[Entity]) -> List[Entity]:
        out = []
        for e in entities:
            hp: Health = self.entity_manager.get_component(e, Health)
            if not hp.is_dead():
                out.append(e)
        return out

    def is_done(self) -> bool:
        return len(self._living(self.players)) == 0 or len(self._living(self.enemies)) == 0

    def step(self) -> bool:
        if self.is_done():
            winner = "Player" if len(self._living(self.enemies)) == 0 else "Enemy"
            self.log.append(f"Combat ended. Winner: {winner}")
            print(self._render_log())
            return True

        current = self.turn_queue.pop(0)

        current_name = current.name
        current_hp: Health = self.entity_manager.get_component(current, Health)

        # Target selection
        if current in self.players:
            targets = self._living(self.enemies)
        else:
            targets = self._living(self.players)

        target = targets[0]  # sederhana: ambil first yang hidup

        # Enemy AI: auto attack
        cmd = AttackCommand(
            entity_manager=self.entity_manager,
            attacker=current,
            target=target,
            rng=self.rng,
        )
        result = cmd.execute()

        msg = (
            f"{current_name} attacks {target.name} for {result.damage} damage"
            + (" (CRITICAL)" if result.critical else "")
            + f". Target HP: {self.entity_manager.get_component(target, Health).hp}/{self.entity_manager.get_component(target, Health).max_hp}"
        )
        self.log.append(msg)
        print(msg)

        # masukkan kembali
        self.turn_queue.append(current)
        return False

    def _render_log(self) -> str:
        return "\n".join(self.log)

