import subprocess  # Untuk menjalankan aplikasi eksternal
import pyautogui  # Untuk otomatisasi keyboard
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