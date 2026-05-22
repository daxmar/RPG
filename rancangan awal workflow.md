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
