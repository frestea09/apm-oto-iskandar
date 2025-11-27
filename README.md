# Aplikasi Pencarian Pasien RSUD Oto Iskandar Dinata

Aplikasi Tkinter untuk membantu pencarian data pasien serta membuka sistem pendaftaran dan aplikasi BPJS secara cepat.

## Menjalankan aplikasi (mode pengembangan)

1. Pastikan Python 3.11+ sudah terpasang.
2. Instal dependensi utama:
   ```bash
   pip install mysql-connector-python pyautogui
   ```
3. Jalankan aplikasi dari akar repo:
   ```bash
   python main.py
   ```

## Membuat file `.exe` (Windows) dengan PyInstaller

Rekomendasi singkat: lakukan build dari dalam *virtual environment* bersih agar dependensi yang ikut dibundel benar-benar minimal.

1. Buat dan aktifkan virtual environment baru (opsional tapi disarankan):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Pasang dependensi yang dibutuhkan aplikasi dan PyInstaller di dalam lingkungan tersebut:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```
3. Jalankan PyInstaller dari akar repo dengan opsi yang sudah teruji berikut:
   ```bash
   pyinstaller \
     --name "PencarianPasien" \
     --noconsole \
     --onefile \
     --add-data "assets;assets" \
     main.py
   ```
   Keterangan penting:
   - Gunakan tanda titik koma (`;`) pada `--add-data` khusus Windows (contoh di atas). Jika build dari Linux/macOS, gunakan titik dua (`:`) menjadi `--add-data "assets:assets"`.
   - File hasil build tersedia di `dist/` setelah proses selesai. Hapus folder `build/` dan `*.spec` jika ingin melakukan build ulang yang bersih.
4. Jika lokasi Chrome atau aplikasi BPJS berbeda dari default, perbarui nilainya di `app/config.py` sebelum menjalankan PyInstaller agar ikut tertanam di executable.
5. Uji hasil build pada mesin Windows target dengan membuka `dist/PencarianPasien.exe`. Pastikan dependency eksternal (Chrome dan aplikasi BPJS) sudah terpasang di mesin pengguna.

## Catatan tambahan

- Pada saat runtime, aplikasi akan membuka jendela Chrome di sisi kanan layar dan jendela Tkinter di sisi kiri dengan lebar 50% layar serta tinggi penuh.
- Untuk menguji build, jalankan langsung file `.exe` pada mesin Windows yang memiliki resolusi layar yang cukup agar kedua jendela bisa tampil berdampingan.
