from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Health:
    hp: int
    max_hp: int

    def is_dead(self) -> bool:
        return self.hp <= 0


@dataclass
class Stats:
    strength: int
    defense: int
    agility: int
    crit_chance: float = 0.1
    crit_multiplier: float = 1.5


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Inventory:
    items: list[str]

