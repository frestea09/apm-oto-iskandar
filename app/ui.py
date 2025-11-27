"""Tkinter UI for patient lookup and BPJS automation."""
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import sys
import os

from app import bpjs, database, network
from app.config import CHECKIN_URL, CHROME_EXECUTABLE


class PatientApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistem APM RSUD OTO ISKANDAR DINATA")
        self.root.configure(background="#ffffff", padx=20, pady=20, height=5, width=5)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.half_screen_width = max(self.screen_width // 2, 1)
        self.root.geometry(f"{self.half_screen_width}x{self.screen_height}+0+0")

        # Menentukan lokasi assets
        if getattr(sys, 'frozen', False):
            # Jika aplikasi dijalankan sebagai file bundel (.exe)
            bundle_dir = sys._MEIPASS
        else:
            # Jika aplikasi dijalankan dari source code
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        # Path lengkap ke file gambar
        image_path = os.path.join(bundle_dir, 'assets', 'logo_dua.png')

        self.logo_image = tk.PhotoImage(file=image_path)

        self.root.iconphoto(False, self.logo_image)

        self.no_rm_var = tk.StringVar()
        self.loading_var = tk.StringVar(value="")
        self._keypad_buttons: list[tk.Button] = []

        self._build_inputs()
        self._build_status()

        self.refresh_status()

    def _build_inputs(self):
        header = tk.Frame(self.root, bg="#ffffff")
        header.pack(pady=(0, 6))

        logo_label = tk.Label(header, image=self.logo_image, bg="#ffffff")
        logo_label.pack(side=tk.LEFT, padx=(0, 10))

        title = tk.Label(
            header,
            text="Layanan Check-In Pasien",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
        )
        title.pack(side=tk.LEFT)

        subtitle = tk.Label(
            self.root,
            text=(
                "Masukkan No. Rekam Medis, NIK, atau nomor BPJS.\n"
                "Tekan tombol sesuai kebutuhan, lalu ikuti langkah check-in."
            ),
            font=("Helvetica", 11),
            bg="#ffffff",
            fg="#3a3a3a",
            justify=tk.CENTER,
        )
        subtitle.pack(pady=(0, 12))

        entry_frame = tk.Frame(self.root, bg="#ffffff")
        entry_frame.pack(pady=6)

        label_no_rm = tk.Label(
            entry_frame,
            text="Nomor Identitas Pasien",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
        )
        label_no_rm.grid(row=0, column=0, sticky="w", padx=(0, 10))

        entry_no_rm = tk.Entry(
            entry_frame,
            textvariable=self.no_rm_var,
            width=35,
            font=("Helvetica", 14),
            bd=2,
            relief=tk.GROOVE,
        )
        entry_no_rm.grid(row=1, column=0,ipadx=5,ipady=7, padx=(0, 10), pady=5, sticky="we")
        self.no_rm_entry = entry_no_rm

        keypad_frame = tk.Frame(self.root, bg="#ffffff")
        keypad_frame.pack(pady=5)

        keypad_layout = [
            ("1", self._append_digit),
            ("2", self._append_digit),
            ("3", self._append_digit),
            ("4", self._append_digit),
            ("5", self._append_digit),
            ("6", self._append_digit),
            ("7", self._append_digit),
            ("8", self._append_digit),
            ("9", self._append_digit),
            ("Clear", self._clear_input),
            ("0", self._append_digit),
            ("Del", self._delete_last_digit),
        ]

        for index, (label, handler) in enumerate(keypad_layout):
            is_action = label in {"Clear", "Del"}
            bg_color = "#ffd6e0" if label == "Clear" else "#ffe8cc" if label == "Del" else "#ffffff"
            button = tk.Button(
                keypad_frame,
                text=label,
                width=8,
                height=2,
                font=("Helvetica", 12, "bold"),
                bg=bg_color,
                command=(
                    lambda l=label, h=handler, action=is_action: h(l)
                    if not action
                    else h()
                ),
            )
            button.grid(row=index // 3, column=index % 3, padx=4, pady=4, sticky="nsew")
            self._keypad_buttons.append(button)

        for column_index in range(3):
            keypad_frame.grid_columnconfigure(column_index, weight=1)

        action_frame = tk.Frame(self.root, bg="#ffffff")
        action_frame.pack(pady=12)

        self.search_button = tk.Button(
            action_frame,
            text="Cari Data Pasien",
            font=("Helvetica", 12, "bold"),
            width=25,
            height=2,
            bg="#d9f2ff",
            command=self.search_patient,
        )
        self.search_button.grid(row=0, column=0, padx=8, pady=6)

        self.open_bpjs_button = tk.Button(
            action_frame,
            text="Buka Check-In BPJS",
            font=("Helvetica", 12, "bold"),
            width=25,
            height=2,
            bg="#c8f7c5",
            command=self.open_bpjs_by_identifier,
        )
        self.open_bpjs_button.grid(row=0, column=1, padx=8, pady=6)

        self.open_checkin_portal_button = tk.Button(
            action_frame,
            text="Buka Sistem Pendaftaran",
            font=("Helvetica", 12, "bold"),
            width=25,
            height=2,
            bg="#fff2b2",
            command=self.open_checkin_portal,
        )
        self.open_checkin_portal_button.grid(row=1, column=0, columnspan=2, padx=8, pady=(6, 2))

        loading_label = tk.Label(
            self.root,
            textvariable=self.loading_var,
            fg="#0057a4",
            bg="#f7f8fa",
            font=("Helvetica", 11, "italic"),
        )
        loading_label.pack(pady=(4, 12))

    def _build_status(self):
        self.internet_status = tk.Label(self.root, text="Internet: Memeriksa...", fg="orange")
        self.internet_status.pack(pady=10)

        self.db_status = tk.Label(self.root, text="Database: Memeriksa...", fg="orange")
        self.db_status.pack(pady=10)

    def refresh_status(self):
        if network.has_internet_connection():
            self.internet_status.config(text="Internet: Terhubung", fg="green")
        else:
            self.internet_status.config(text="Internet: Tidak Terhubung", fg="red")

        connection_ok = database.ping_database()

        if connection_ok:
            self.db_status.config(text="Database: Tersedia", fg="green")
        else:
            self.db_status.config(text="Database: Tidak Tersedia", fg="red")

    def search_patient(self):
        no_rm = self.no_rm_var.get().strip()
        if not no_rm:
            messagebox.showwarning("Input Error", "Nomor Rekam Medis (no_rm) tidak boleh kosong.")
            return

        try:
            patient = database.fetch_patient_by_no_rm(no_rm)
        except Exception as err:
            messagebox.showerror("Database Error", f"Terjadi kesalahan: {err}")
            return

        if patient:
            patient_info = (
                f"Nama: {patient[3]}\n"
                f"Tgl Lahir: {patient[5]}\n"
                f"Alamat: {patient[7]}\n"
                f"Golongan Darah: {patient[8]}"
            )
            messagebox.showinfo("Hasil Pencarian", patient_info)
        else:
            messagebox.showinfo("Hasil Pencarian", "Pasien dengan No RM tersebut tidak ditemukan.")

    def open_bpjs_by_member_id(self):
        no_rm = self.no_rm_var.get().strip()
        if not no_rm:
            messagebox.showwarning("Input Error", "Nomor Rekam Medis tidak boleh kosong.")
            return

        self._run_bpjs_action(lambda: bpjs.open_bpjs_for_member_id(no_rm), "Membuka aplikasi BPJS...")

    def open_bpjs_by_identifier(self):
        identifier = self.no_rm_var.get().strip()
        if not identifier:
            messagebox.showwarning("Input Error", "Masukkan No RM, NIK, atau BPJS terlebih dahulu.")
            return

        self._run_bpjs_action(lambda: bpjs.open_bpjs_for_identifier(identifier), "Membuka aplikasi BPJS...")

    def open_checkin_portal(self):
        self._run_bpjs_action(self._launch_checkin_portal, "Membuka sistem pendaftaran...")

    def _launch_checkin_portal(self):
        window_position = f"--window-position={self.half_screen_width},0"
        window_size = f"--window-size={self.half_screen_width},{self.screen_height}"
        subprocess.Popen(
            [
                CHROME_EXECUTABLE,
                window_position,
                window_size,
                "--new-window",
                CHECKIN_URL,
            ]
        )

    def _run_bpjs_action(self, action, message: str):
        self._set_loading_state(True, message)

        def task():
            try:
                action()
            except Exception as error:  # noqa: BLE001
                bpjs.handle_automation_error(error)
            finally:
                self.root.after(0, lambda: self._set_loading_state(False))

        threading.Thread(target=task, daemon=True).start()

    def _set_loading_state(self, is_loading: bool, message: str | None = None):
        if is_loading:
            if message is not None:
                self.loading_var.set(message)
        else:
            self.loading_var.set("")

        state = tk.DISABLED if is_loading else tk.NORMAL
        self.search_button.config(state=state)
        self.open_bpjs_button.config(state=state)
        self.open_checkin_portal_button.config(state=state)
        for button in self._keypad_buttons:
            button.config(state=state)
        self.root.update_idletasks()

    def _append_digit(self, digit: str):
        current = self.no_rm_var.get()
        self.no_rm_var.set(current + digit)
        self.no_rm_entry.icursor(tk.END)

    def _delete_last_digit(self):
        current = self.no_rm_var.get()
        self.no_rm_var.set(current[:-1])
        self.no_rm_entry.icursor(tk.END)

    def _clear_input(self):
        self.no_rm_var.set("")
        self.no_rm_entry.icursor(tk.END)
