"""Tkinter UI for patient lookup and BPJS automation."""
import threading
import tkinter as tk
from tkinter import messagebox

from app import bpjs, database, network


class PatientApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pencarian Pasien")

        self.no_rm_var = tk.StringVar()
        self.loading_var = tk.StringVar(value="")
        self._digit_buttons: list[tk.Button] = []

        self._build_inputs()
        self._build_status()

        self.refresh_status()

    def _build_inputs(self):
        label_no_rm = tk.Label(self.root, text="Masukkan No Rekam Medis / NIK / BPJS Anda:")
        label_no_rm.pack(pady=10)

        entry_no_rm = tk.Entry(self.root, textvariable=self.no_rm_var, width=30)
        entry_no_rm.pack(pady=5)
        self.no_rm_entry = entry_no_rm

        keypad_frame = tk.Frame(self.root)
        keypad_frame.pack(pady=5)
        digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for index, digit in enumerate(digits):
            button = tk.Button(
                keypad_frame,
                text=digit,
                width=4,
                command=lambda d=digit: self._append_digit(d),
            )
            button.grid(row=index // 3, column=index % 3, padx=3, pady=3)
            self._digit_buttons.append(button)

        self.search_button = tk.Button(self.root, text="Cari Pasien", command=self.search_patient)
        self.search_button.pack(pady=20)

        self.open_bpjs_button = tk.Button(
            self.root,
            text="Buka Aplikasi BPJS",
            command=self.open_bpjs_by_identifier,
        )
        self.open_bpjs_button.pack(pady=10)

        loading_label = tk.Label(self.root, textvariable=self.loading_var, fg="blue")
        loading_label.pack(pady=(0, 10))

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

        self._run_bpjs_action(lambda: bpjs.open_bpjs_for_member_id(no_rm))

    def open_bpjs_by_identifier(self):
        identifier = self.no_rm_var.get().strip()
        if not identifier:
            messagebox.showwarning("Input Error", "Masukkan No RM, NIK, atau BPJS terlebih dahulu.")
            return

        self._run_bpjs_action(lambda: bpjs.open_bpjs_for_identifier(identifier))

    def _run_bpjs_action(self, action):
        self._set_loading_state(True, "Membuka aplikasi BPJS...")

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
        for button in self._digit_buttons:
            button.config(state=state)
        self.root.update_idletasks()

    def _append_digit(self, digit: str):
        current = self.no_rm_var.get()
        self.no_rm_var.set(current + digit)
        self.no_rm_entry.icursor(tk.END)
