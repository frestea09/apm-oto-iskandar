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

1. Pasang PyInstaller (disarankan di dalam virtual environment):
   ```bash
   pip install pyinstaller
   ```
2. Dari akar repo, jalankan perintah berikut untuk membuat executable tanpa jendela konsol:
   ```bash
   pyinstaller \
     --name "PencarianPasien" \
     --noconsole \
     --onefile \
     --add-data "assets;assets" \
     main.py
   ```
   Keterangan penting:
   - Gunakan tanda titik koma (`;`) sebagai pemisah sumber/tujuan pada opsi `--add-data` di Windows agar folder `assets` ikut terbawa.
   - File hasil build bisa ditemukan di folder `dist/` setelah proses selesai.
3. Jika aplikasi membutuhkan lokasi Chrome atau BPJS yang berbeda, perbarui nilai di `app/config.py` sebelum membangun.
4. Distribusikan `dist/PencarianPasien.exe` ke pengguna. Pastikan dependency eksternal (seperti instalasi Google Chrome dan aplikasi BPJS) sudah tersedia di komputer pengguna.

## Catatan tambahan

- Pada saat runtime, aplikasi akan membuka jendela Chrome di sisi kanan layar dan jendela Tkinter di sisi kiri dengan lebar 50% layar serta tinggi penuh.
- Untuk menguji build, jalankan langsung file `.exe` pada mesin Windows yang memiliki resolusi layar yang cukup agar kedua jendela bisa tampil berdampingan.
