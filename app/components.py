"""Reusable UI components for the patient app."""

import tkinter as tk


def create_keypad(root: tk.Tk, append_digit, clear_input, delete_last):
    keypad_frame = tk.Frame(root, bg="#ffffff")
    keypad_frame.pack(pady=5)

    buttons: list[tk.Button] = []
    keypad_layout = [
        ("1", append_digit),
        ("2", append_digit),
        ("3", append_digit),
        ("4", append_digit),
        ("5", append_digit),
        ("6", append_digit),
        ("7", append_digit),
        ("8", append_digit),
        ("9", append_digit),
        ("Clear", clear_input),
        ("0", append_digit),
        ("Del", delete_last),
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
            command=(lambda l=label, h=handler, action=is_action: h(l) if not action else h()),
        )
        button.grid(row=index // 3, column=index % 3, padx=4, pady=4, sticky="nsew")
        buttons.append(button)

    for column_index in range(3):
        keypad_frame.grid_columnconfigure(column_index, weight=1)

    return buttons


def create_action_buttons(root: tk.Tk, on_bpjs, on_portal, on_frista):
    action_frame = tk.Frame(root, bg="#ffffff")
    action_frame.pack(pady=16, fill=tk.X)

    button_opts = {"font": ("Helvetica", 13, "bold"), "width": 30, "height": 3, "anchor": "center"}

    bpjs_button = tk.Button(action_frame, text="Fingerprint BPJS", bg="#c8f7c5", command=on_bpjs, **button_opts)
    bpjs_button.pack(padx=8, pady=6, fill=tk.X)

    portal_button = tk.Button(
        action_frame, text="Sistem Pendaftaran", bg="#fff2b2", command=on_portal, **button_opts
    )
    portal_button.pack(padx=8, pady=6, fill=tk.X)

    frista_button = tk.Button(action_frame, text="Frista", bg="#e8d2ff", command=on_frista, **button_opts)
    frista_button.pack(padx=8, pady=6, fill=tk.X)
    return bpjs_button, portal_button, frista_button
