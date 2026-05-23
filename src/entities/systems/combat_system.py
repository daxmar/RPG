import random
from src.entities.components import Health, Stats, Name

class Command:
    """Base class untuk aksi dalam combat"""
    def execute(self):
        pass
    def undo(self):
        pass

class AttackCommand(Command):
    def __init__(self, attacker, target):
        self.attacker = attacker
        self.target = target
        self.damage_dealt = 0
        self.is_critical = False
        self.prev_hp = 0
        self.log = ""

    def execute(self):
        attacker_stats = self.attacker.get_component(Stats)
        target_stats = self.target.get_component(Stats)
        target_health = self.target.get_component(Health)
        attacker_name = self.attacker.get_component(Name).value
        target_name = self.target.get_component(Name).value

        self.prev_hp = target_health.current
        
        # Kalkulasi Damage: (Str - Def) dengan minimal 1 damage
        base_damage = max(1, attacker_stats.strength - target_stats.defense)
        
        # Kalkulasi Critical
        if random.random() < attacker_stats.critical_chance:
            self.is_critical = True
            base_damage *= 2
        
        self.damage_dealt = base_damage
        target_health.current = max(0, target_health.current - self.damage_dealt)
        
        crit_text = "CRITICAL HIT! " if self.is_critical else ""
        self.log = f"{crit_text}{attacker_name} menyerang {target_name} sebesar {self.damage_dealt} DMG."
        return self.log

    def undo(self):
        target_health = self.target.get_component(Health)
        target_health.current = self.prev_hp
        return f"Undo: {self.target.get_component(Name).value} HP kembali ke {self.prev_hp}"

class CombatManager:
    def __init__(self, entities):
        self.entities = entities
        self.turn_queue = []
        self.history = []
        self.generate_queue()

    def generate_queue(self):
        # Urutan berdasarkan Agility (tertinggi pertama)
        self.turn_queue = sorted(
            [e for e in self.entities if e.has_component(Stats)],
            key=lambda e: e.get_component(Stats).agility,
            reverse=True
        )

    def get_current_entity(self):
        if not self.turn_queue:
            self.generate_queue()
        return self.turn_queue[0]

    def end_turn(self):
        if self.turn_queue:
            entity = self.turn_queue.pop(0)
            self.turn_queue.append(entity)

    def perform_action(self, command):
        result = command.execute()
        self.history.append(command)
        self.end_turn()
        return result