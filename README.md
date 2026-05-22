# Aetheria RPG (Minimal Prototype)

Ini adalah realisasi awal dari dokumen workflow yang ada di repo.

## Yang sudah dibuat
- Kerangka project Python
- ECS minimal (Entity + Components + EntityManager)
- Turn-based Combat minimal (CombatManager + AttackCommand)
- State machine minimal (Menu -> Combat -> Exit)
- Data-driven loader untuk konten (contoh `data/monsters.json`)

## Cara menjalankan

### Prasyarat
- Python 3.10+ direkomendasikan

### Jalankan
```bash
python main.py
```

Jika pygame belum terpasang, game akan tetap berjalan dalam mode headless (log ke terminal).
