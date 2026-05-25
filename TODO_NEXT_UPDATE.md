# Rencana Update Selanjutnya (lanjutan)

## Target
Membuat prototipe game berjalan stabil dan siap ditambah fitur berikutnya sesuai TODO.

## Step 1 — Stabilkan loop combat (sudah dilakukan sebagian)
- Pastikan `StateManager` memanggil `CombatManager.step()` yang sesuai.
- Pastikan log combat dan HUD membaca field komponen yang benar (`Health.current/max`, `Stats.critical_chance`).
- Pastikan combat pasti selesai (win/lose) lalu state pindah ke `exit`.

## Step 2 — Matangkan data-driven entities
- Buat mapping data monster JSON ke komponen ECS (HP/Stats) secara konsisten.
- Tambahkan `Name` component (bila dibutuhkan) agar log memakai nama dari data, bukan `entity.name`.

## Step 3 — Rapikan API ECS (menghapus potensi duplikasi)
- Hindari dua implementasi `Entity`/`EntityManager` yang berbeda (dataclass-vs-uuid).
- Pilih satu implementasi ECS saja agar sistem tidak pernah salah metode.

## Step 4 — Tingkatkan CombatManager
- Turn order: skip entity mati sudah ada; tambahkan re-generate queue jika perlu.
- Pilih target: saat ini memilih HP terendah; bisa dibuat strategi AI.
- Tambah aksi lain: skill/defend/heal (masih sederhana dulu).

## Step 5 — Integrasi UI
- Pastikan `CombatLog` menampilkan `combat.log` (format list[str]) konsisten.
- Jika pygame mode digunakan, pastikan event loop tidak “hang”.

## Step 6 — Mulai Tahap Eksplorasi/Map (TODO Tahap 6)
- Tambah `map_generator.py` (cellular automata / drunkard’s walk).
- Tambah `MovementSystem` (input WASD/arrow) dan `Camera` mengikuti player.

---

Catatan: dokument ini adalah rencana lanjutan setelah update kompatibilitas combat dan ECS.

