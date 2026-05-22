1. Rancangan Alur Kerja Proyek (Workflow)
Pengembangan akan dibagi menjadi beberapa fase modular:

Fase 1: Core Engine & State Management
Mengatur Game Loop (FPS, event handling).
State Machine: Mengatur perpindahan antara Menu Utama, Eksplorasi Dunia, dan Mode Pertarungan.
Fase 2: Sistem Entitas (ECS - Entity Component System)
Menggunakan pola ECS agar karakter, musuh, dan item sangat fleksibel.
Entity: ID unik. Component: Data (Health, Position, Inventory). System: Logika (MovementSystem, CombatSystem).
Fase 3: Data & Content Driven
Semua data item, musuh, dan dialog disimpan dalam file JSON/YAML agar mudah diubah tanpa menyentuh kode program.
Fase 4: Rendering & GUI
Menggunakan pygame-ce atau arcade untuk visual 2D.
Sistem kamera top-down atau isometric.

2. Logika Utama (Core Logic)
A. Logika Pertarungan (Turn-Based Combat)
Menggunakan sistem Action Point (AP) atau Initiative Queue.

# Logika dasar urutan giliran
class CombatManager:
    def __init__(self, players, enemies):
        self.entities = players + enemies
        self.turn_queue = sorted(self.entities, key=lambda x: x.stats['agility'], reverse=True)

    def next_turn(self):
        current_entity = self.turn_queue.pop(0)
        # Proses AI jika musuh, atau tunggu input jika player
        self.turn_queue.append(current_entity) # Masukkan kembali ke antrian

C. Logika Dialog & Quest (State Machine)
Menggunakan tree structure untuk percabangan cerita.

3. Struktur Folder Proyek (Skala Kompleks)

Aetheria/
├── assets/             # Gambar, Sound, Font
├── data/               # JSON untuk item.json, monsters.json, quests.json
├── src/
│   ├── core/           # engine.py, state_manager.py, camera.py
│   ├── entities/       # entity.py, components.py, systems/
│   ├── ui/             # menu.py, hud.py, dialogue_box.py
│   ├── worlds/         # map_loader.py, tile_system.py
│   └── utils/          # constants.py, helpers.py
└── main.py             # Entry point

4. Catatan Pengembangan (Dev Log)
Optimasi Rendering: Gunakan Sprite Groups dan Dirty Sprite rendering di Pygame agar game tetap lancar meski banyak objek di layar.
Save System: Gunakan modul pickle atau json untuk menyimpan status PlayerComponent dan WorldState.
Pathfinding: Implementasikan algoritma A* (A-Star) untuk pergerakan NPC dan musuh agar tidak menabrak tembok.
Event Bus: Buat sistem pengiriman pesan global (misal: saat monster mati, kirim pesan ke QuestSystem untuk update progress).