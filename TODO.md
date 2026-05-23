# TODO - RPG Project

## Tahap 1: Kerangka Proyek
- [x] Buat struktur folder: `src/core`, `src/entities`, `src/ui`, `src/worlds`, `src/utils`, `data`, `assets`
- [x] Buat `main.py` sebagai entrypoint
- [x] Buat `src/core/state_manager.py` untuk state machine: Menu -> Combat -> Exit

## Tahap 2: ECS & Data Model Minimal
- [x] Buat `src/entities/entity.py` (Entity + id)
- [x] Buat `src/entities/components.py` (dataclasses: Health, Position, Stats, Inventory)
- [x] Buat `src/entities/entity_manager.py`

## Tahap 3: Combat Turn-Based Minimal
- [x] Buat `src/entities/systems/combat_system.py`
- [x] Buat `CombatManager` / queue berbasis `agility`
- [x] Implement `AttackCommand` menggunakan Command Pattern + log/undo sederhana
- [x] Buat perhitungan damage: `Strength` vs `Defense`, critical hit

## Tahap 4: Data-driven Loader
- [x] Buat `src/worlds/data_loader.py` untuk membaca JSON dari `data/`
- [x] Buat `data/monsters.json` contoh

## Tahap 5: Rendering & UI (Minimal)
- [x] Buat `src/ui/hud.py` (HP + turn info)
- [x] Buat `src/ui/dialogue_box.py` atau overlay untuk log combat
- [x] Integrasi pygame loop ke state manager

## Tahap 6: Sistem Eksplorasi & Map (Sedang Dikerjakan)
- [ ] Buat `src/worlds/map_generator.py` menggunakan Cellular Automata/Drunkard's Walk
- [ ] Implementasi sistem Kamera agar mengikuti pergerakan entitas Player
- [ ] Buat `MovementSystem` untuk menangani input arah (WASD/Arrows) di map

## Tahap 7: Perluasan ECS & Sistem RPG
- [ ] Tambahkan `InventoryComponent` dan `ItemComponent`
- [ ] Buat `SkillSystem`: Dukungan untuk Mana/MP dan serangan spesial (area/heal)
- [ ] Implementasi Status Effects (Poison, Stun, Buff) di dalam `CombatManager`
- [ ] Buat sistem Leveling & Experience (XP)

## Tahap 8: Persistence & UI Lanjut
- [ ] Buat `src/utils/save_manager.py` untuk Save/Load via JSON (terenkripsi sederhana)
- [ ] Buat UI Menu Inventory yang interaktif
- [ ] Tambahkan transisi antar layar (Fade in/out) menggunakan state manager

## Tahap 9: Content & Polish
- [ ] Buat `data/items.json` dan `data/skills.json`
- [ ] Tambahkan aset visual (Sprites) dan Sound Effects (SFX)
- [ ] Implementasi AI musuh yang lebih cerdas (memilih target HP terendah atau menggunakan skill)
- [ ] Final validasi gameplay loop: Explore -> Combat -> Loot -> Level Up -> Explore
