"""Database helpers for patient lookup."""
from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Iterable, Optional, Tuple

import mysql.connector

from app.config import DB_CONFIG


PatientRow = Tuple
RegistrationRow = Tuple

ERROR_LOG_PATH = Path.home() / "apm_db_errors.log"

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(ERROR_LOG_PATH, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def ping_database() -> tuple[bool, Optional[str]]:
    try:
        with mysql_connection():
            return True, None
    except mysql.connector.Error as err:
        if err.errno == 2059 and "mysql_native_password" in str(err):
            error_message = (
                "Plugin autentikasi mysql_native_password belum aktif di server. "
                "Perbarui user MySQL yang dipakai aplikasi agar memakai plugin tersebut, "
                "contoh perintah: ALTER USER '<user>'@'%' IDENTIFIED WITH "
                "mysql_native_password BY '<password>'; lalu FLUSH PRIVILEGES. "
                "Connector sudah dibundel di aplikasi, tidak perlu install tambahan di PC."
            )
        else:
            error_message = f"{err}"
        logger.error("Database ping failed: %s", error_message)
        return False, error_message
    except Exception as err:  # noqa: BLE001
        error_message = f"Kesalahan tidak terduga: {err}"
        logger.exception(error_message)
        return False, error_message


@contextmanager
def mysql_connection():
    """Context manager returning a MySQL connection."""
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        if conn.is_connected():
            conn.close()


def fetch_one(query: str, params: Iterable) -> Optional[Tuple]:
    with mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result


def fetch_patient_by_no_rm(no_rm: str) -> Optional[PatientRow]:
    return fetch_one("SELECT * FROM pasiens WHERE no_rm = %s", (no_rm,))


def fetch_patient_by_nik(nik: str) -> Optional[PatientRow]:
    return fetch_one("SELECT * FROM pasiens WHERE nik = %s", (nik,))


def fetch_registration_by_no_rm(no_rm: str) -> Optional[RegistrationRow]:
    """Fetch the newest registration matching the given medical record number."""
    return fetch_one(
        "SELECT * FROM registrasis_dummy WHERE no_rm = %s ORDER BY id DESC LIMIT 1",
        (no_rm,),
    )


def fetch_registration_by_nik(nik: str) -> Optional[RegistrationRow]:
    """Fetch the newest registration matching the given national ID."""
    return fetch_one(
        "SELECT * FROM registrasis_dummy WHERE nik = %s ORDER BY id DESC LIMIT 1",
        (nik,),
    )


def fetch_registration_by_bpjs(bpjs_number: str) -> Optional[RegistrationRow]:
    """Fetch the newest registration matching the given BPJS card number."""
    return fetch_one(
        "SELECT * FROM registrasis_dummy WHERE nomorkartu = %s ORDER BY id DESC LIMIT 1",
        (bpjs_number,),
    )


def fetch_patient_by_bpjs(bpjs_number: str) -> Optional[PatientRow]:
    """Fetch a patient record by BPJS card number."""
    return fetch_one("SELECT * FROM pasiens WHERE no_jkn = %s", (bpjs_number,))
