"""Automation helpers for BPJS fingerprint application."""
import subprocess
from typing import Optional

import pyautogui
from tkinter import messagebox

from app import database
from app.config import (
    BPJS_EXECUTABLE,
    BPJS_PASSWORD,
    BPJS_USERNAME,
    FORM_FILL_DELAY_SECONDS,
    LOGIN_DELAY_SECONDS,
    POST_LOGIN_DELAY_SECONDS,
)


class BpjsAutomationError(Exception):
    """Raised when automation cannot proceed due to missing data."""


def _launch_application():
    subprocess.Popen([BPJS_EXECUTABLE])
    pyautogui.sleep(1.5)


def _login():
    pyautogui.sleep(LOGIN_DELAY_SECONDS)
    pyautogui.write(BPJS_USERNAME)
    pyautogui.press("tab")
    pyautogui.write(BPJS_PASSWORD)
    pyautogui.press("enter")
    pyautogui.sleep(POST_LOGIN_DELAY_SECONDS)
    pyautogui.press("enter")


def _focus_window():
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)


def _fill_member_id(member_id: str):
    _focus_window()
    for _ in range(4):
        pyautogui.press("tab")
    pyautogui.press("space")
    pyautogui.write(member_id)
    pyautogui.sleep(FORM_FILL_DELAY_SECONDS)
    pyautogui.hotkey("alt", "f4")


def _fill_registration_details(registration: Optional[tuple], patient: Optional[tuple]):
    _focus_window()
    if registration and registration[3]:
        pyautogui.write(registration[3])
    if patient and len(patient) > 32 and patient[32]:
        if(len(patient[32])!=1):
            pyautogui.write(patient[32])
        else:
            pyautogui.press("tab")
            pyautogui.press("tab")
            pyautogui.press("tab")
            pyautogui.press("tab")
            pyautogui.press("space")
            pyautogui.write(patient[36])
    pyautogui.sleep(FORM_FILL_DELAY_SECONDS)
    pyautogui.hotkey("alt", "f4")


def _extract_nik_from_patient(patient: tuple) -> Optional[str]:
    """Return the first 16-digit numeric field found in the patient tuple."""

    for field in patient:
        if isinstance(field, str) and len(field) == 16 and field.isdigit():
            return field
    return None


def open_bpjs_for_member_id(no_rm: str):
    patient = database.fetch_patient_by_no_rm(no_rm)
    if not patient:
        raise BpjsAutomationError("Pasien dengan No RM tersebut tidak ditemukan.")

    if len(patient) <= 36 or not patient[36]:
        raise BpjsAutomationError("Data BPJS untuk pasien tidak tersedia.")

    _launch_application()
    _login()
    _fill_member_id(patient[36])


def open_bpjs_for_identifier(identifier: str):
    if not identifier:
        raise BpjsAutomationError("Masukkan No RM, NIK, atau BPJS terlebih dahulu.")

    registration: Optional[tuple] = None
    patient: Optional[tuple] = None

    registration = database.fetch_registration_by_no_rm(identifier)
    patient = database.fetch_patient_by_no_rm(identifier)

    if len(identifier) == 16:
        registration = registration or database.fetch_registration_by_nik(identifier)
        patient = patient or database.fetch_patient_by_nik(identifier)

    registration = registration or database.fetch_registration_by_bpjs(identifier)
    patient = patient or database.fetch_patient_by_bpjs(identifier)

    if not registration and not patient:
        raise BpjsAutomationError("Data registrasi atau pasien tidak ditemukan.")

    nik = None
    if len(identifier) == 16 and identifier.isdigit():
        nik = identifier
    if not nik and patient:
        nik = _extract_nik_from_patient(patient)

    _launch_application()
    _login()

    if registration:
        _fill_registration_details(registration, patient)
    elif patient and len(patient) > 32 and patient[32]:
        _fill_registration_details(None, patient)
    elif nik:
        _fill_member_id(nik)
    else:
        raise BpjsAutomationError("NIK untuk pasien tidak ditemukan.")


def handle_automation_error(error: Exception):
    messagebox.showerror("Error", f"Terjadi kesalahan saat membuka aplikasi: {error}")
