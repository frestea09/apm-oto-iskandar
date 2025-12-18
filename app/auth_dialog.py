"""Authentication dialog for admin access."""

import tkinter as tk
from tkinter import messagebox


def prompt_admin_login(root: tk.Tk) -> bool:
    dialog = tk.Toplevel(root)
    dialog.title("Autentikasi Admin")
    dialog.transient(root)
    dialog.grab_set()

    content = tk.Frame(dialog, padx=12, pady=12)
    content.pack(fill=tk.BOTH, expand=True)

    tk.Label(content, text="Username").grid(row=0, column=0, sticky="w", pady=4, padx=(0, 8))
    username_var = tk.StringVar()
    username_entry = tk.Entry(content, textvariable=username_var, width=30)
    username_entry.grid(row=0, column=1, pady=4, sticky="we")

    tk.Label(content, text="Password").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 8))
    password_var = tk.StringVar()
    password_entry = tk.Entry(content, textvariable=password_var, width=30, show="*")
    password_entry.grid(row=1, column=1, pady=4, sticky="we")

    result = {"ok": False}

    def submit():
        if username_var.get().strip() == "admin" and password_var.get() == "123456":
            result["ok"] = True
            dialog.destroy()
        else:
            messagebox.showerror("Autentikasi", "Username atau password salah.")

    button_frame = tk.Frame(content)
    button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

    tk.Button(button_frame, text="Masuk", command=submit, width=12).pack(side=tk.LEFT, padx=6)
    tk.Button(button_frame, text="Batal", command=dialog.destroy, width=12).pack(side=tk.LEFT, padx=6)

    dialog.bind("<Return>", lambda _event: submit())
    username_entry.focus_set()
    dialog.wait_window()
    return result["ok"]
