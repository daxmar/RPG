Instruksi AI untuk Pengembangan Selanjutnya
Jika Anda ingin memberikan proyek ini ke AI (seperti Gemini atau ChatGPT) untuk dilanjutkan, gunakan prompt yang sangat spesifik seperti berikut:


Prompt A (Untuk Membuat Sistem Combat):

"Tolong buatkan modul combat_system.py berbasis turn-based untuk RPG Python. Gunakan pola Command Pattern agar setiap aksi (Attack, Skill, Item) bisa di-undo atau di-log. Integrasikan dengan sistem kalkulasi damage yang dipengaruhi oleh stat 'Strength' penyerang dan 'Defense' target, termasuk probabilitas 'Critical Hit'."

Prompt B (Untuk Membuat Map Procedural):

"Buatlah kelas MapGenerator menggunakan algoritma Cellular Automata untuk membuat dungeon gua secara acak. Outputnya harus berupa array 2D yang bisa dibaca oleh sistem TileMap Pygame. Pastikan ada pengecekan konektivitas agar tidak ada area yang terisolasi."

Prompt C (Untuk Save/Load System):

"Buatlah fungsi save_game dan load_game yang mengonversi seluruh objek dalam EntityManager (khususnya komponen Player, Inventory, dan QuestFlags) ke dalam format JSON terenkripsi sederhana untuk mencegah tampering."

