from dataclasses import dataclass

@dataclass
class Name:
    value: str

@dataclass
class Health:
    current: int
    max: int

@dataclass
class Stats:
    strength: int
    defense: int
    agility: int
    critical_chance: float = 0.1  # 10% default

@dataclass
class Position:
    x: int
    y: int