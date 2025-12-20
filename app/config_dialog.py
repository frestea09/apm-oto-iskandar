"""Configuration dialog handling."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from app import config


def _initial_dir_from(var: tk.StringVar) -> Path:
    try:
        candidate = Path(var.get()).expanduser()
        if candidate.is_file():
            return candidate.parent
        if candidate.exists():
            return candidate
    except OSError:
        pass
    return Path.home()


def _clean_path(value: str) -> str:
    return value.replace("\\\\", "\\").strip()


def _choose_file(var: tk.StringVar):
    initial_dir = _initial_dir_from(var)
    selected = filedialog.askopenfilename(
        initialdir=str(initial_dir), filetypes=[("Executable", "*.exe"), ("All Files", "*.*")]
    )
    if selected:
        var.set(_clean_path(selected))


def open_config_dialog(root: tk.Tk):
    dialog = tk.Toplevel(root)
    dialog.title("Pengaturan")
    dialog.transient(root)
    dialog.grab_set()

    entries = {
        "BPJS Executable": tk.StringVar(value=config.BPJS_EXECUTABLE),
        "BPJS Username": tk.StringVar(value=config.BPJS_USERNAME),
        "BPJS Password": tk.StringVar(value=config.BPJS_PASSWORD),
        "Standby BPJS Setelah Login (detik)": tk.StringVar(value=str(config.BPJS_STANDBY_SECONDS)),
        "Chrome Executable": tk.StringVar(value=config.CHROME_EXECUTABLE),
        "URL Sistem Pendaftaran": tk.StringVar(value=config.CHECKIN_URL),
        "URL Cek SEP": tk.StringVar(value=config.SEP_CHECK_URL),
        "URL Dasar Aplikasi APM": tk.StringVar(value=config.SEP_BASE_URL),
        "Frista Executable": tk.StringVar(value=config.FRISTA_EXECUTABLE),
        "Frista Username": tk.StringVar(value=config.FRISTA_USERNAME),
        "Frista Password": tk.StringVar(value=config.FRISTA_PASSWORD),
        "Standby Frista Setelah Login (detik)": tk.StringVar(value=str(config.FRISTA_STANDBY_SECONDS)),
        "Penundaan Login Frista (detik)": tk.StringVar(value=str(config.FRISTA_LOGIN_DELAY_SECONDS)),
    }

    content = tk.Frame(dialog, padx=10, pady=10)
    content.pack(fill=tk.BOTH, expand=True)

    for index, (label_text, var) in enumerate(entries.items()):
        tk.Label(content, text=label_text, anchor="w").grid(row=index, column=0, sticky="w", pady=4, padx=(0, 8))
        entry_frame = tk.Frame(content)
        entry_frame.grid(row=index, column=1, sticky="we", pady=4)
        entry_frame.grid_columnconfigure(0, weight=1)

        tk.Entry(entry_frame, textvariable=var, width=55).grid(row=0, column=0, sticky="we")
        if label_text in {"BPJS Executable", "Chrome Executable", "Frista Executable"}:
            tk.Button(entry_frame, text="Browse...", command=lambda v=var: _choose_file(v), width=10).grid(
                row=0, column=1, padx=(6, 0)
            )

    button_frame = tk.Frame(content)
    button_frame.grid(row=len(entries), column=0, columnspan=2, pady=(12, 0))

    def save_config():
        try:
            updated_settings = {
                "BPJS_EXECUTABLE": _clean_path(entries["BPJS Executable"].get()),
                "BPJS_USERNAME": entries["BPJS Username"].get(),
                "BPJS_PASSWORD": entries["BPJS Password"].get(),
                "BPJS_STANDBY_SECONDS": float(entries["Standby BPJS Setelah Login (detik)"].get()),
                "CHROME_EXECUTABLE": _clean_path(entries["Chrome Executable"].get()),
                "CHECKIN_URL": entries["URL Sistem Pendaftaran"].get(),
                "SEP_CHECK_URL": entries["URL Cek SEP"].get(),
                "SEP_BASE_URL": entries["URL Dasar Aplikasi APM"].get(),
                "FRISTA_EXECUTABLE": _clean_path(entries["Frista Executable"].get()),
                "FRISTA_USERNAME": entries["Frista Username"].get(),
                "FRISTA_PASSWORD": entries["Frista Password"].get(),
                "FRISTA_STANDBY_SECONDS": float(entries["Standby Frista Setelah Login (detik)"].get()),
                "FRISTA_LOGIN_DELAY_SECONDS": float(entries["Penundaan Login Frista (detik)"].get()),
            }
        except ValueError:
            messagebox.showerror(
                "Pengaturan",
                "Masukkan angka yang valid untuk pengaturan durasi standby atau penundaan login.",
            )
            return

        try:
            config.save_user_settings(updated_settings)
        except OSError as error:  # noqa: BLE001
            messagebox.showerror("Pengaturan", f"Gagal menyimpan konfigurasi: {error}")
            return

        messagebox.showinfo("Pengaturan", "Konfigurasi berhasil diperbarui.")
        dialog.destroy()

    tk.Button(button_frame, text="Simpan", command=save_config, width=12).pack(side=tk.LEFT, padx=6)
    tk.Button(button_frame, text="Tutup", command=dialog.destroy, width=12).pack(side=tk.LEFT, padx=6)
