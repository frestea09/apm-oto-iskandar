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
     --collect-all mysql.connector \
     main.py
   ```
   Atau gunakan `main.spec` yang sudah disiapkan untuk otomatis membawa modul
   `mysql.connector` saat build onefile:
   ```bash
   pyinstaller main.spec
   ```
   Keterangan penting:
  - Gunakan tanda titik koma (`;`) pada `--add-data` khusus Windows (contoh di atas). Jika build dari Linux/macOS, gunakan titik dua (`:`) menjadi `--add-data "assets:assets"`.
  - File hasil build tersedia di `dist/` setelah proses selesai. Hapus folder `build/` dan `*.spec` jika ingin melakukan build ulang yang bersih.
  - Plugin autentikasi `caching_sha2_password` sudah diimpor eksplisit di kode dan disertakan di `main.spec` agar ikut terbawa ke executable PyInstaller.
4. Jika lokasi Chrome atau aplikasi BPJS berbeda dari default, perbarui nilainya di `app/config.py` sebelum menjalankan PyInstaller agar ikut tertanam di executable.
5. Uji hasil build pada mesin Windows target dengan membuka `dist/PencarianPasien.exe`. Pastikan dependency eksternal (Chrome dan aplikasi BPJS) sudah terpasang di mesin pengguna.

## Alternatif build Windows dengan py2exe

Jika lebih nyaman memakai `py2exe`, skrip `setup_py2exe.py` sudah disiapkan agar modul `mysql.connector` dan folder `assets` ikut dibawa dalam output. Jalankan perintah berikut di Command Prompt/PowerShell Windows dari akar repo.

1. Aktifkan virtual environment (opsional tapi disarankan) dan pasang py2exe:
   ```bash
   pip install -r requirements.txt
   pip install py2exe
   ```
   Jika muncul pesan `error: invalid command 'py2exe'` atau peringatan opsi distribusi
   tidak dikenal, pastikan perintah di atas sudah dijalankan pada Python Windows.
2. Jalankan build:
   ```bash
   python setup_py2exe.py py2exe --bundle 1 --dist-dir dist_py2exe
   ```
   Keterangan:
   - `--bundle 1` menghasilkan satu executable (mirip opsi `--onefile` di PyInstaller). Hilangkan opsi ini jika ingin melihat file-file dependency terpisah.
   - Output tersalin ke folder `dist_py2exe/` dengan struktur `PencarianPasien.exe` dan subfolder `assets` di sampingnya agar logo/gambar terbaca.
   - Jika ingin build ulang yang bersih, hapus folder `build/` dan `dist_py2exe/` sebelum menjalankan perintah di atas.
3. Uji `dist_py2exe/PencarianPasien.exe` di mesin target. Pastikan MySQL server dapat diakses dan plugin `mysql_native_password` sudah diaktifkan sesuai panduan sebelumnya.

## Catatan tambahan

- Pada saat runtime, aplikasi akan membuka jendela Chrome di sisi kanan layar dan jendela Tkinter di sisi kiri dengan lebar 50% layar serta tinggi penuh.
- Untuk menguji build, jalankan langsung file `.exe` pada mesin Windows yang memiliki resolusi layar yang cukup agar kedua jendela bisa tampil berdampingan.
