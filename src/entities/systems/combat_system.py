import random
from src.entities.components import Health, Stats


class Command:
    """Base class untuk aksi dalam combat"""
    def execute(self):
        pass
    def undo(self):
        pass

class AttackCommand(Command):
    def __init__(self, entity_manager, attacker, target):
        self.entity_manager = entity_manager
        self.attacker = attacker
        self.target = target
        self.damage_dealt = 0
        self.is_critical = False
        self.prev_hp = 0
        self.log = ""

    def execute(self):
        attacker_stats = self.entity_manager.get_component(self.attacker, Stats)
        target_stats = self.entity_manager.get_component(self.target, Stats)
        target_health = self.entity_manager.get_component(self.target, Health)

        self.prev_hp = target_health.current

        # Kalkulasi Damage: (Str - Def) dengan minimal 1 damage
        base_damage = max(1, attacker_stats.strength - target_stats.defense)

        # Kalkulasi Critical
        if random.random() < attacker_stats.critical_chance:
            self.is_critical = True
            # desain saat ini: critical = 2x damage (konsisten dengan implementasi sebelumnya)
            base_damage *= 2

        self.damage_dealt = base_damage
        target_health.current = max(0, target_health.current - self.damage_dealt)

        attacker_name = getattr(self.attacker, "name", "Attacker")
        target_name = getattr(self.target, "name", "Target")

        crit_text = "CRITICAL HIT! " if self.is_critical else ""
        self.log = f"{crit_text}{attacker_name} menyerang {target_name} sebesar {self.damage_dealt} DMG."
        return self.log

    def undo(self):
        target_health = self.entity_manager.get_component(self.target, Health)
        target_health.current = self.prev_hp
        return f"Undo: {getattr(self.target, 'name', 'Target')} HP kembali ke {self.prev_hp}"

class CombatManager:
    def __init__(
        self,
        entity_manager,
        players,
        enemies,
    ):
        self.entity_manager = entity_manager
        self.players = list(players)
        self.enemies = list(enemies)
        self.entities = self.players + self.enemies

        self.turn_queue: list = []
        self.history = []
        self.log: list[str] = []
        self.turn_index = 0

        self.generate_queue()

    def generate_queue(self):
        # Urutan berdasarkan Agility (tertinggi pertama)
        self.turn_queue = sorted(
            [e for e in self.entities if self.entity_manager.has_component(e, Stats)],
            key=lambda e: self.entity_manager.get_component(e, Stats).agility,
            reverse=True,
        )

    def get_current_entity(self):
        if not self.turn_queue:
            self.generate_queue()
        return self.turn_queue[0]

    def end_turn(self):
        if self.turn_queue:
            entity = self.turn_queue.pop(0)
            self.turn_queue.append(entity)

    def _is_defeated(self, entity) -> bool:
        if not self.entity_manager.has_component(entity, Health):
            return False
        hp: Health = self.entity_manager.get_component(entity, Health)
        return hp.current <= 0

    def _choose_target(self, attacker):
        # attacker -> pihak lawan
        is_player = attacker in self.players
        candidates = self.enemies if is_player else self.players
        alive = [e for e in candidates if not self._is_defeated(e)]
        if not alive:
            return None
        # target dengan HP terendah
        alive.sort(key=lambda e: self.entity_manager.get_component(e, Health).current)
        return alive[0]

    def step(self) -> bool:
        """Return True jika combat selesai."""
        if not self.turn_queue:
            self.generate_queue()

        attacker = self.get_current_entity()
        if self._is_defeated(attacker):
            # skip kalau mati (agar tidak stuck)
            self.end_turn()
            return self._check_end()

        target = self._choose_target(attacker)
        if target is None:
            return True

        command = AttackCommand(self.entity_manager, attacker, target)
        result = command.execute()
        self.history.append(command)
        self.log.append(result)
        self.turn_index += 1

        self.end_turn()
        return self._check_end()

    def _check_end(self) -> bool:
        any_player_alive = any(not self._is_defeated(p) for p in self.players)
        any_enemy_alive = any(not self._is_defeated(e) for e in self.enemies)
        return not (any_player_alive and any_enemy_alive)
