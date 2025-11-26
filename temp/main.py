import configparser
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

DEFAULT_FRISTA_PATH = "frista.exe"
DEFAULT_AFTER_PATH = r"C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe"
SETTINGS_FILE = Path("settings.ini")


def load_settings():
    config = configparser.ConfigParser()
    frista_path = DEFAULT_FRISTA_PATH
    after_path = DEFAULT_AFTER_PATH

    if SETTINGS_FILE.exists():
        config.read(SETTINGS_FILE)
        frista_path = config.get("Paths", "Frista", fallback=DEFAULT_FRISTA_PATH)
        after_path = config.get("Paths", "After", fallback=DEFAULT_AFTER_PATH)

    return frista_path, after_path


def save_settings(frista_path: str, after_path: str) -> None:
    config = configparser.ConfigParser()
    config["Paths"] = {"Frista": frista_path, "After": after_path}
    with SETTINGS_FILE.open("w", encoding="utf-8") as config_file:
        config.write(config_file)


def launch_executable(path: str, description: str) -> None:
    try:
        subprocess.Popen(path, shell=True)
    except OSError as exc:
        messagebox.showerror("Gagal", f"Tidak dapat membuka {description}: {exc}")
    else:
        messagebox.showinfo("Berhasil", f"{description} sedang dibuka…")


def open_settings(root: tk.Tk, frista_var: tk.StringVar, after_var: tk.StringVar) -> None:
    window = tk.Toplevel(root)
    window.title("Pengaturan Aplikasi")
    window.geometry("500x220")

    tk.Label(window, text="Frista Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    frista_entry = tk.Entry(window, textvariable=frista_var, width=50)
    frista_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(window, text="After Path:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    after_entry = tk.Entry(window, textvariable=after_var, width=50)
    after_entry.grid(row=1, column=1, padx=10, pady=10)

    def browse_file(var: tk.StringVar):
        filepath = filedialog.askopenfilename(filetypes=[("Executable", "*.exe"), ("All files", "*.*")])
        if filepath:
            var.set(filepath)

    tk.Button(window, text="Browse", command=lambda: browse_file(frista_var)).grid(row=0, column=2, padx=5, pady=10)
    tk.Button(window, text="Browse", command=lambda: browse_file(after_var)).grid(row=1, column=2, padx=5, pady=10)

    def save_and_close():
        save_settings(frista_var.get(), after_var.get())
        messagebox.showinfo("Sukses", "Pengaturan disimpan.")
        window.destroy()

    action_frame = tk.Frame(window)
    action_frame.grid(row=3, column=0, columnspan=3, pady=20)
    tk.Button(action_frame, text="Simpan", command=save_and_close, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(action_frame, text="Batal", command=window.destroy, width=12).pack(side=tk.LEFT, padx=10)


def main():
    frista_path, after_path = load_settings()

    root = tk.Tk()
    root.title("Mesin Layanan BPJS - Mudah Digunakan")
    root.configure(bg="white")
    root.attributes("-fullscreen", True)

    frista_var = tk.StringVar(value=frista_path)
    after_var = tk.StringVar(value=after_path)

    menubar = tk.Menu(root)
    app_menu = tk.Menu(menubar, tearoff=0)
    app_menu.add_command(label="Buka Aplikasi", command=lambda: launch_executable(frista_var.get(), "Aplikasi Frista"))
    app_menu.add_command(label="Pengaturan Aplikasi", command=lambda: open_settings(root, frista_var, after_var))
    menubar.add_cascade(label="Menu", menu=app_menu)
    root.config(menu=menubar)

    header = tk.Label(
        root,
        text="Selamat datang di Mesin Layanan BPJS. Ikuti langkah-langkah berikut:",
        font=("Arial", 20, "bold"),
        bg="white",
    )
    header.pack(pady=(30, 20))

    tk.Label(root, text="Masukkan Nomor BPJS Anda:", font=("Arial", 16), bg="white").pack(pady=(10, 5))
    bpjs_var = tk.StringVar()
    bpjs_entry = tk.Entry(root, textvariable=bpjs_var, font=("Arial", 18), width=40)
    bpjs_entry.pack(pady=(0, 20))

    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="Login dan Verifikasi Wajah (Frista)",
        font=("Arial", 16, "bold"),
        command=lambda: launch_executable(frista_var.get(), "Aplikasi Frista"),
        width=40,
        pady=10,
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="Isi Data Sidik Jari (Registrasi)",
        font=("Arial", 16, "bold"),
        command=lambda: launch_executable(after_var.get(), "Aplikasi After"),
        width=40,
        pady=10,
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="Print Tiket",
        font=("Arial", 16, "bold"),
        command=lambda: launch_executable(
            r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe http://172.168.1.175:8070",
            "Halaman Pendaftaran Online",
        ),
        width=40,
        pady=10,
    ).pack(pady=10)

    tk.Label(
        root,
        text="Pastikan Anda memiliki kartu BPJS dan siap untuk verifikasi wajah atau sidik jari.",
        font=("Arial", 14),
        bg="white",
    ).pack(pady=10)

    tk.Button(
        root,
        text="Keluar",
        font=("Arial", 16, "bold"),
        command=root.destroy,
        width=30,
        pady=10,
    ).pack(pady=20)

    tk.Label(
        root,
        text="© 2025 SIMRS RSUD Otista Soreang",
        font=("Arial", 14),
        fg="#808080",
        bg="white",
    ).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
