import tkinter as tk
from tkinter import messagebox
import mysql.connector
import socket
import os
import subprocess  # Untuk menjalankan aplikasi eksternal
import pyautogui  # Untuk otomatisasi keyboard
# Fungsi untuk memeriksa koneksi internet
def check_internet():
    try:
        # Mencoba melakukan ping ke google.com untuk mengecek koneksi internet
        socket.create_connection(("www.google.com", 80), timeout=5)
        internet_status.config(text="Internet: Terhubung", fg="green")
    except (socket.timeout, socket.error):
        internet_status.config(text="Internet: Tidak Terhubung", fg="red")

# Fungsi untuk memeriksa koneksi MySQL
def check_mysql_connection():
    try:
        # Coba untuk menghubungkan ke database MySQL
        conn = mysql.connector.connect(
            host="172.168.1.2",      # IP server MySQL
            user="root",             # Nama pengguna
            password="s1mrs234@",    # Password
            database="otista_dev",   # Nama database
            port=3306                # Ganti dengan port yang ditemukan, jika berbeda
        )
        conn.close()
        db_status.config(text="Database: Tersedia", fg="green")
    except mysql.connector.Error as err:
        db_status.config(text="Database: Tidak Tersedia", fg="red")

# Fungsi untuk melakukan pencarian pasien berdasarkan no_rm
def search_patient():
    # Ambil nomor rekam medis yang dimasukkan oleh pengguna
    no_rm = entry_no_rm.get()

    # Periksa apakah no_rm kosong
    if not no_rm:
        messagebox.showwarning("Input Error", "Nomor Rekam Medis (no_rm) tidak boleh kosong.")
        return

    try:
        # Koneksi ke database MySQL
        conn = mysql.connector.connect(
            host="172.168.1.2",      # IP server MySQL
            user="root",             # Nama pengguna
            password="s1mrs234@",    # Password
            database="otista_dev",   # Nama database
            port=3306                # Ganti dengan port yang ditemukan, jika berbeda
        )

        cursor = conn.cursor()

        # Query untuk mencari pasien berdasarkan no_rm
        query = "SELECT * FROM pasiens WHERE no_rm = %s"
        cursor.execute(query, (no_rm,))

        # Ambil hasil pencarian
        result = cursor.fetchone()

        # Tampilkan hasil pencarian
        if result:
            print(result)
            patient_info = f"Nama: {result[3]}\nTgl Lahir: {result[5]}\nAlamat: {result[7]}\nGolongan Darah: {result[8]}"
            messagebox.showinfo("Hasil Pencarian", patient_info)
        else:
            messagebox.showinfo("Hasil Pencarian", "Pasien dengan No RM tersebut tidak ditemukan.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Terjadi kesalahan: {err}")
    finally:
        # Menutup koneksi database
        if conn.is_connected():
            cursor.close()
            conn.close()

def open_bpjs_application():
    
    try:
        
        # Jalankan file executable (.exe)
        subprocess.Popen(["C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe"])
        no_rm = entry_no_rm.get()
        conn = mysql.connector.connect(
            host="172.168.1.2",      # IP server MySQL
            user="root",             # Nama pengguna
            password="s1mrs234@",    # Password
            database="otista_dev",   # Nama database
            port=3306                # Ganti dengan port yang ditemukan, jika berbeda
        )

        cursor = conn.cursor()
        query = "SELECT * FROM pasiens WHERE no_rm = %s"
        cursor.execute(query, (no_rm,))
        result = cursor.fetchone()
        # Tunggu beberapa detik untuk memastikan aplikasi terbuka
        pyautogui.sleep(1)  # Menunggu 2 detik untuk aplikasi terbuka

        # Isi username
        pyautogui.write('1002r006th')  # Username
        pyautogui.press('tab')  # Tekan Tab untuk berpindah ke kolom password
        
        # Isi password
        pyautogui.write('#Bandung28')  # Password
        pyautogui.press('enter')  # Tekan Enter untuk login

        pyautogui.sleep(1)  # Tunggu sebentar agar login berhasil
        pyautogui.press('enter')  # Tekan Enter untuk login
        screen_width, screen_height = pyautogui.size()  # Dapatkan resolusi layar
        pyautogui.click(screen_width // 2, screen_height // 2)  # Klik kiri di tengah layar
        pyautogui.press('tab')  # Tekan Tab untuk berpindah ke kolom password
        pyautogui.press('tab')  # Tekan Tab untuk berpindah ke kolom password
        pyautogui.press('tab')  # Tekan Tab untuk berpindah ke kolom password
        pyautogui.press('tab')  # Tekan Tab untuk berpindah ke kolom password
        pyautogui.press('space')  # Tekan Tab untuk berpindah ke kolom password
        pyautogui.write(result[36])
        pyautogui.sleep(5)
        pyautogui.hotkey('alt', 'f4')  # Menekan Alt + F4 untuk menutup aplikasi BPJS
     

        # messagebox.showinfo("Aplikasi BPJS", "Aplikasi BPJS Frista berhasil dibuka dan login berhasil!")
    
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat membuka aplikasi: {e}")

def open_bpjs_application_bpjs():
    
    try:
        
        # Jalankan file executable (.exe)
        subprocess.Popen(["C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe"])
        no_rm = entry_no_rm.get()
        conn = mysql.connector.connect(
            host="172.168.1.2",      # IP server MySQL
            user="root",             # Nama pengguna
            password="s1mrs234@",    # Password
            database="otista_dev",   # Nama database
            port=3306                # Ganti dengan port yang ditemukan, jika berbeda
        )
        if(len(no_rm)!=16):
            cursor = conn.cursor()
            query = "SELECT * FROM registrasis_dummy WHERE no_rm = %s"
            cursor.execute(query, (no_rm,))
            result = cursor.fetchone()
            query = "SELECT * FROM pasiens WHERE no_rm = %s"
            resultjkan = cursor.fetchone()
            # Tunggu beberapa detik untuk memastikan aplikasi terbuka
            pyautogui.sleep(1)  # Menunggu 2 detik untuk aplikasi terbuka

            # Isi username
            pyautogui.write('1002r006th')  # Username
            pyautogui.press('tab')  # Tekan Tab untuk berpindah ke kolom password
            
            # Isi password
            pyautogui.write('#Bandung28')  # Password
            pyautogui.press('enter')  # Tekan Enter untuk login

            pyautogui.sleep(1)  # Tunggu sebentar agar login berhasil
            pyautogui.press('enter')  # Tekan Enter untuk login
            screen_width, screen_height = pyautogui.size()  # Dapatkan resolusi layar
            pyautogui.click(screen_width // 2, screen_height // 2)  # Klik kiri di tengah layar
            if(result[3]):
                pyautogui.write(result[3])
            if(resultjkan[32]):
                pyautogui.write(resultjkan[32])
            pyautogui.sleep(5)
            pyautogui.hotkey('alt', 'f4')  # Menekan Alt + F4 untuk menutup aplikasi BPJS
        else:
            cursor = conn.cursor()
            query = "SELECT * FROM registrasis_dummy WHERE nik = %s"
            cursor.execute(query, (no_rm,))
            result = cursor.fetchone()
            query = "SELECT * FROM pasiens WHERE no_rm = %s"
            resultjkan = cursor.fetchone()
            # Tunggu beberapa detik untuk memastikan aplikasi terbuka
            pyautogui.sleep(1)  # Menunggu 2 detik untuk aplikasi terbuka

            # Isi username
            pyautogui.write('1002r006th')  # Username
            pyautogui.press('tab')  # Tekan Tab untuk berpindah ke kolom password
            
            # Isi password
            pyautogui.write('#Bandung28')  # Password
            pyautogui.press('enter')  # Tekan Enter untuk login

            pyautogui.sleep(1)  # Tunggu sebentar agar login berhasil
            pyautogui.press('enter')  # Tekan Enter untuk login
            screen_width, screen_height = pyautogui.size()  # Dapatkan resolusi layar
            pyautogui.click(screen_width // 2, screen_height // 2)  # Klik kiri di tengah layar
            if(result[3]):
                pyautogui.write(result[3])
            if(resultjkan[32]):
                pyautogui.write(resultjkan[32])
            pyautogui.sleep(5)
            pyautogui.hotkey('alt', 'f4')  # Menekan Alt + F4 untuk menutup aplikasi BPJS
    
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat membuka aplikasi: {e}")
# Membuat aplikasi GUI dengan Tkinter
root = tk.Tk()
root.title("Pencarian Pasien")

# Label untuk input no_rm
label_no_rm = tk.Label(root, text="Masukkan No RM:")
label_no_rm.pack(pady=10)

# Entry untuk memasukkan no_rm
entry_no_rm = tk.Entry(root, width=30)
entry_no_rm.pack(pady=5)

# Tombol untuk mencari pasien
search_button = tk.Button(root, text="Cari Pasien", command=search_patient)
search_button.pack(pady=20)

# Indikator Koneksi Internet
internet_status = tk.Label(root, text="Internet: Memeriksa...", fg="orange")
internet_status.pack(pady=10)

# Indikator Koneksi Database
db_status = tk.Label(root, text="Database: Memeriksa...", fg="orange")
db_status.pack(pady=10)

# Tombol untuk membuka aplikasi BPJS (Frista.exe)
open_bpjs_button = tk.Button(root, text="Buka Aplikasi BPJS", command=open_bpjs_application)
open_bpjs_button.pack(pady=20)

open_bpjs_button_by_nik = tk.Button(root, text="NIK", command=open_bpjs_application_bpjs)
open_bpjs_button_by_nik.pack(pady=20)
# Periksa status internet dan database saat aplikasi dimulai
check_internet()
check_mysql_connection()

# Menjalankan aplikasi Tkinter
root.mainloop() 