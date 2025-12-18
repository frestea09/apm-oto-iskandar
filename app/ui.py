"""Tkinter UI for patient lookup and BPJS automation."""

import tkinter as tk
from tkinter import messagebox

from app import actions, bpjs, database, frista, network
from app import auth_dialog, components, config_dialog, layout


class PatientApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logo_image = layout.load_logo_image()

        self.no_rm_var = tk.StringVar()
        self.loading_var = tk.StringVar(value="")

        self.half_screen_width, self.screen_height = layout.setup_root(root, self.logo_image)

        self.no_rm_entry = layout.create_input_section(root, self.logo_image, self.no_rm_var)
        self._keypad_buttons = components.create_keypad(
            root, self._append_digit, self._clear_input, self._delete_last_digit
        )
        (
            self.open_bpjs_button,
            self.open_checkin_portal_button,
            self.open_frista_button,
        ) = components.create_action_buttons(
            root, self.open_bpjs_by_identifier, self.open_checkin_portal, self.open_frista_application
        )

        self.internet_status, self.db_status = layout.create_status_section(root, self.loading_var)

        self._create_menu()
        self.refresh_status()

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="Pengaturan...", command=self._open_config_dialog)
        menubar.add_cascade(label="Config", menu=config_menu)
        self.root.config(menu=menubar)

    def refresh_status(self):
        if network.has_internet_connection():
            self.internet_status.config(text="Internet: Terhubung", fg="green")
        else:
            self.internet_status.config(text="Internet: Tidak Terhubung", fg="red")

        connection_ok, db_error = database.ping_database()
        if connection_ok:
            self.db_status.config(text="Database: Tersedia", fg="green")
        else:
            self.db_status.config(text="Database: Tidak Tersedia", fg="red")
            if db_error:
                messagebox.showerror(
                    "Database Error",
                    (
                        "Aplikasi tidak dapat terhubung ke database.\n"
                        f"Detail: {db_error}\n"
                        f"Log kesalahan: {database.ERROR_LOG_PATH}"
                    ),
                )

    def open_bpjs_by_identifier(self):
        identifier = self.no_rm_var.get().strip()
        if not identifier:
            messagebox.showwarning("Input Error", "Masukkan No RM, NIK, atau BPJS terlebih dahulu.")
            return
        self._run_bpjs_action(lambda: bpjs.open_bpjs_for_identifier(identifier), "Membuka aplikasi BPJS...")

    def open_checkin_portal(self):
        actions.run_action(
            self.root,
            self._set_loading_state,
            lambda: actions.launch_checkin_portal(self.half_screen_width, self.screen_height),
            "Membuka sistem pendaftaran...",
            self._action_buttons,
        )

    def open_frista_application(self):
        identifier = self.no_rm_var.get().strip()
        if not identifier:
            messagebox.showwarning("Input Error", "Masukkan NIK atau identitas pasien terlebih dahulu.")
            return
        actions.run_action(
            self.root,
            self._set_loading_state,
            lambda: frista.open_frista_for_identifier(identifier),
            "Membuka Frista...",
            self._action_buttons,
            frista.handle_automation_error,
        )

    def _run_bpjs_action(self, action, message: str):
        actions.run_bpjs_action(self.root, self._set_loading_state, action, message, self._action_buttons)

    def _set_loading_state(self, is_loading: bool, message: str | None = None, buttons=None):
        if is_loading:
            if message is not None:
                self.loading_var.set(message)
        else:
            self.loading_var.set("")

        targets = buttons or []
        for button in targets:
            button.config(state=tk.DISABLED if is_loading else tk.NORMAL)
        for button in self._keypad_buttons:
            button.config(state=tk.DISABLED if is_loading else tk.NORMAL)
        self.root.update_idletasks()

    @property
    def _action_buttons(self):
        return [self.open_bpjs_button, self.open_checkin_portal_button, self.open_frista_button]

    def _append_digit(self, digit: str):
        self.no_rm_var.set(self.no_rm_var.get() + digit)
        self.no_rm_entry.icursor(tk.END)

    def _delete_last_digit(self):
        self.no_rm_var.set(self.no_rm_var.get()[:-1])
        self.no_rm_entry.icursor(tk.END)

    def _clear_input(self):
        self.no_rm_var.set("")
        self.no_rm_entry.icursor(tk.END)

    def _open_config_dialog(self):
        if auth_dialog.prompt_admin_login(self.root):
            config_dialog.open_config_dialog(self.root)
