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
    target_width = min(int(screen_width * 0.75), screen_width - 40)
    target_height = min(int(screen_height * 0.9), screen_height - 80)
    half_screen_width = max(screen_width // 2, 1)
    root.geometry(f"{target_width}x{target_height}+0+0")
    root.minsize(max(target_width // 2, min(screen_width - 80, 600)), max(target_height // 2, 480))
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.iconphoto(False, logo_image)
    return half_screen_width, screen_height


def create_main_frames(root: tk.Tk) -> tuple[tk.Frame, tk.Frame]:
    content = tk.Frame(root, bg="#ffffff")
    content.grid(row=0, column=0, sticky="nsew")
    content.columnconfigure(0, weight=3, minsize=360)
    content.columnconfigure(1, weight=2, minsize=300)
    content.rowconfigure(0, weight=1)

    left_panel = tk.Frame(content, bg="#ffffff")
    right_panel = tk.Frame(content, bg="#ffffff")
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    right_panel.grid(row=0, column=1, sticky="nsew")
    right_panel.rowconfigure(0, weight=1)
    right_panel.rowconfigure(1, weight=0)
    right_panel.columnconfigure(0, weight=1)
    return left_panel, right_panel


def create_input_section(parent: tk.Frame, logo_image: tk.PhotoImage, no_rm_var: tk.StringVar):
    header = tk.Frame(parent, bg="#ffffff")
    header.pack(pady=(0, 6), fill=tk.X)

    tk.Label(header, image=logo_image, bg="#ffffff").pack(side=tk.LEFT, padx=(0, 10))
    tk.Label(header, text="Layanan Check-In Pasien", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(
        side=tk.LEFT
    )

    tk.Label(
        parent,
        text=(
            "Masukkan No. Rekam Medis, NIK, atau nomor BPJS.\n"
            "Tekan tombol sesuai kebutuhan, lalu ikuti langkah check-in."
        ),
        font=("Helvetica", 11),
        bg="#ffffff",
        fg="#3a3a3a",
        justify=tk.CENTER,
        wraplength=540,
    ).pack(pady=(0, 12), fill=tk.X)

    entry_frame = tk.Frame(parent, bg="#ffffff")
    entry_frame.pack(pady=6, fill=tk.X)
    tk.Label(entry_frame, text="Nomor Identitas Pasien", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(
        row=0, column=0, sticky="w", padx=(0, 10)
    )

    entry_no_rm = tk.Entry(entry_frame, textvariable=no_rm_var, font=("Helvetica", 14), bd=2, relief=tk.GROOVE)
    entry_no_rm.grid(row=1, column=0, ipadx=5, ipady=7, padx=(0, 10), pady=5, sticky="we")
    entry_frame.grid_columnconfigure(0, weight=1)
    return entry_no_rm


def create_status_section(parent: tk.Frame, loading_var: tk.StringVar):
    status_frame = tk.Frame(parent, bg="#ffffff")
    status_frame.grid_columnconfigure(0, weight=1)
    tk.Label(
        status_frame, textvariable=loading_var, fg="#0057a4", bg="#f7f8fa", font=("Helvetica", 11, "italic")
    ).pack(pady=(4, 12), fill=tk.X)
    internet_status = tk.Label(status_frame, text="Internet: Memeriksa...", fg="orange", bg="#ffffff", anchor="w")
    internet_status.pack(pady=6, fill=tk.X)

    db_status = tk.Label(status_frame, text="Database: Memeriksa...", fg="orange", bg="#ffffff", anchor="w")
    db_status.pack(pady=6, fill=tk.X)
    return status_frame, internet_status, db_status
