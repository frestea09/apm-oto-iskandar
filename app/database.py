"""Database helpers for patient lookup."""
from contextlib import contextmanager
from typing import Iterable, Optional, Tuple

import mysql.connector

from app.config import DB_CONFIG


PatientRow = Tuple
RegistrationRow = Tuple


def ping_database() -> bool:
    try:
        with mysql_connection():
            return True
    except mysql.connector.Error:
        return False


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
    return fetch_one("SELECT * FROM registrasis_dummy WHERE no_rm = %s", (no_rm,))


def fetch_registration_by_nik(nik: str) -> Optional[RegistrationRow]:
    return fetch_one("SELECT * FROM registrasis_dummy WHERE nik = %s", (nik,))
