"""Root window preparation and shared layout helpers."""

from pathlib import Path
import sys
import tkinter as tk


def load_logo_image() -> tk.PhotoImage:
    if getattr(sys, "_MEIPASS", None):
        assets_root = Path(sys._MEIPASS)
    elif getattr(sys, "frozen", False):
        assets_root = Path(sys.executable).resolve().parent
    else:
        assets_root = Path(__file__).resolve().parent.parent

    return tk.PhotoImage(file=str((assets_root / "assets" / "logo_dua.png").resolve()))


def setup_root(root: tk.Tk, logo_image: tk.PhotoImage) -> tuple[int, int]:
    root.title("Sistem APM RSUD OTO ISKANDAR DINATA")
    root.configure(background="#ffffff", padx=20, pady=20, height=5, width=5)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    half_screen_width = max(screen_width // 2, 1)
    root.geometry(f"{half_screen_width}x{screen_height}+0+0")
    root.iconphoto(False, logo_image)
    return half_screen_width, screen_height


def create_input_section(root: tk.Tk, logo_image: tk.PhotoImage, no_rm_var: tk.StringVar):
    header = tk.Frame(root, bg="#ffffff")
    header.pack(pady=(0, 6))

    tk.Label(header, image=logo_image, bg="#ffffff").pack(side=tk.LEFT, padx=(0, 10))
    tk.Label(header, text="Layanan Check-In Pasien", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(
        side=tk.LEFT
    )

    tk.Label(
        root,
        text=(
            "Masukkan No. Rekam Medis, NIK, atau nomor BPJS.\n"
            "Tekan tombol sesuai kebutuhan, lalu ikuti langkah check-in."
        ),
        font=("Helvetica", 11),
        bg="#ffffff",
        fg="#3a3a3a",
        justify=tk.CENTER,
    ).pack(pady=(0, 12))

    entry_frame = tk.Frame(root, bg="#ffffff")
    entry_frame.pack(pady=6)
    tk.Label(entry_frame, text="Nomor Identitas Pasien", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(
        row=0, column=0, sticky="w", padx=(0, 10)
    )

    entry_no_rm = tk.Entry(entry_frame, textvariable=no_rm_var, width=35, font=("Helvetica", 14), bd=2, relief=tk.GROOVE)
    entry_no_rm.grid(row=1, column=0, ipadx=5, ipady=7, padx=(0, 10), pady=5, sticky="we")
    return entry_no_rm


def create_status_section(root: tk.Tk, loading_var: tk.StringVar):
    tk.Label(root, textvariable=loading_var, fg="#0057a4", bg="#f7f8fa", font=("Helvetica", 11, "italic")).pack(
        pady=(4, 12)
    )
    internet_status = tk.Label(root, text="Internet: Memeriksa...", fg="orange")
    internet_status.pack(pady=10)

    db_status = tk.Label(root, text="Database: Memeriksa...", fg="orange")
    db_status.pack(pady=10)
    return internet_status, db_status
