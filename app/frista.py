"""Automation helpers for launching and filling the Frista application."""
import subprocess

import pyautogui
from tkinter import messagebox

from app import config


class FristaAutomationError(Exception):
    """Raised when Frista automation cannot proceed."""


def open_frista_for_identifier(identifier: str):
    """Launch Frista and fill credentials plus the provided identifier."""

    if not identifier:
        raise FristaAutomationError("Masukkan NIK atau identitas pasien terlebih dahulu.")

    try:
        subprocess.Popen([config.FRISTA_EXECUTABLE])
    except FileNotFoundError as exc:
        raise FristaAutomationError("Executable Frista tidak ditemukan.") from exc

    pyautogui.sleep(6)
    pyautogui.write(config.FRISTA_USERNAME)
    pyautogui.press("tab")
    pyautogui.write(config.FRISTA_PASSWORD)
    pyautogui.press("tab")
    pyautogui.press("space")

    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)
    pyautogui.write(identifier)


def handle_automation_error(error: Exception):
    messagebox.showerror("Error", f"Terjadi kesalahan saat membuka Frista: {error}")
