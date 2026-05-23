# TODO - RPG Project

## Tahap 1: Kerangka Proyek
- [ ] Buat struktur folder: `src/core`, `src/entities`, `src/ui`, `src/worlds`, `src/utils`, `data`, `assets` (placeholder)
- [ ] Buat `main.py` sebagai entrypoint
- [ ] Buat `src/core/state_manager.py` untuk state machine: Menu -> Combat -> Exit

## Tahap 2: ECS & Data Model Minimal
- [x] Buat `src/entities/entity.py` (Entity + id)
- [x] Buat `src/entities/components.py` (dataclasses: Health, Position, Stats, Inventory)
- [ ] Buat `src/entities/entity_manager.py`

## Tahap 3: Combat Turn-Based Minimal
- [x] Buat `src/entities/systems/combat_system.py`
- [x] Buat `CombatManager` / queue berbasis `agility`
- [x] Implement `AttackCommand` menggunakan Command Pattern + log/undo sederhana
- [x] Buat perhitungan damage: `Strength` vs `Defense`, critical hit

## Tahap 4: Data-driven Loader
- [ ] Buat `src/worlds/data_loader.py` untuk membaca JSON dari `data/`
- [ ] Buat `data/monsters.json` dan `data/items.json` contoh

## Tahap 5: Rendering & UI (Minimal)
- [x] Buat `src/ui/hud.py` (HP + turn info)
- [x] Buat `src/ui/dialogue_box.py` atau overlay untuk log combat
- [x] Integrasi pygame loop ke state manager

## Tahap 6: Run & Validasi
- [ ] Tambahkan `README.md` dengan cara menjalankan
- [x] Jalankan `python main.py` dan pastikan combat berjalan
