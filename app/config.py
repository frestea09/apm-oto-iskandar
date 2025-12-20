"""Central configuration for database and BPJS automation."""

import json
import sys
from pathlib import Path
from typing import Dict

def _config_root() -> Path:
    """Lokasi penyimpanan konfigurasi yang bisa ditulis.

    Saat dijalankan sebagai executable (PyInstaller/py2exe) folder yang dipakai
    adalah direktori executable, bukan direktori bundle sementara yang tidak
    bisa ditulis. Ketika dikembangkan dari sumber, gunakan folder module.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


CONFIG_FILE_PATH = _config_root() / "user_config.json"

# DB_AUTH_PLUGIN = os.environ.get("APM_DB_AUTH_PLUGIN", "mysql_native_password")
DB_AUTH_PLUGIN = "caching_sha2_password"

DB_CONFIG = {
    "host": "172.168.1.2",
    "user": "root",
    "password": "s1mrs234@",
    "database": "otista_dev",
    "port": 3306,
    # Gunakan env APM_DB_AUTH_PLUGIN="caching_sha2_password" bila server sudah default plugin baru
    "auth_plugin": DB_AUTH_PLUGIN,
}

DEFAULT_SETTINGS = {
    "BPJS_EXECUTABLE": r"C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe",
    "BPJS_USERNAME": "1002r006th",
    "BPJS_PASSWORD": "#Bandung28",
    "LOGIN_DELAY_SECONDS": 0.8,
    "POST_LOGIN_DELAY_SECONDS": 0.6,
    "BPJS_STANDBY_SECONDS": 3.0,
    "FORM_FILL_DELAY_SECONDS": 2.5,
    "CHROME_EXECUTABLE": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "CHECKIN_URL": "http://172.168.1.175:8070",
    "SEP_CHECK_URL": "http://172.168.1.175:8070/reservasi/cek",
    "SEP_BASE_URL": "http://172.168.1.175:8070",
    "FRISTA_EXECUTABLE": r"C:\\Users\\ilman\\Documents\\Frista\\Frista.exe",
    "FRISTA_USERNAME": "1002r006th",
    "FRISTA_PASSWORD": "#Bandung28",
    "FRISTA_LOGIN_DELAY_SECONDS": 6.0,
    "FRISTA_STANDBY_SECONDS": 3.0,
}


def _load_user_settings() -> Dict[str, str | float]:
    settings = DEFAULT_SETTINGS.copy()
    if CONFIG_FILE_PATH.exists():
        try:
            loaded = json.loads(CONFIG_FILE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            loaded = {}
        if isinstance(loaded, dict):
            settings.update({k: v for k, v in loaded.items() if k in DEFAULT_SETTINGS})
    return settings


def _persist_settings(settings: Dict[str, str | float]) -> None:
    CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE_PATH.write_text(
        json.dumps(settings, indent=2),
        encoding="utf-8",
    )


def save_user_settings(settings: Dict[str, str | float]) -> None:
    """Persist updated settings and refresh globals for runtime use."""

    DEFAULT_SETTINGS.update(settings)
    _persist_settings(DEFAULT_SETTINGS)
    _apply_settings(DEFAULT_SETTINGS)


def _apply_settings(settings: Dict[str, str | float]) -> None:
    global BPJS_EXECUTABLE
    global BPJS_USERNAME
    global BPJS_PASSWORD
    global LOGIN_DELAY_SECONDS
    global POST_LOGIN_DELAY_SECONDS
    global BPJS_STANDBY_SECONDS
    global FORM_FILL_DELAY_SECONDS
    global CHROME_EXECUTABLE
    global CHECKIN_URL
    global SEP_CHECK_URL
    global SEP_BASE_URL
    global FRISTA_EXECUTABLE
    global FRISTA_USERNAME
    global FRISTA_PASSWORD
    global FRISTA_LOGIN_DELAY_SECONDS
    global FRISTA_STANDBY_SECONDS

    BPJS_EXECUTABLE = settings["BPJS_EXECUTABLE"]
    BPJS_USERNAME = settings["BPJS_USERNAME"]
    BPJS_PASSWORD = settings["BPJS_PASSWORD"]
    LOGIN_DELAY_SECONDS = float(settings["LOGIN_DELAY_SECONDS"])
    POST_LOGIN_DELAY_SECONDS = float(settings["POST_LOGIN_DELAY_SECONDS"])
    BPJS_STANDBY_SECONDS = float(settings["BPJS_STANDBY_SECONDS"])
    FORM_FILL_DELAY_SECONDS = float(settings["FORM_FILL_DELAY_SECONDS"])
    CHROME_EXECUTABLE = settings["CHROME_EXECUTABLE"]
    CHECKIN_URL = settings["CHECKIN_URL"]
    SEP_CHECK_URL = settings["SEP_CHECK_URL"]
    SEP_BASE_URL = settings["SEP_BASE_URL"]
    FRISTA_EXECUTABLE = settings["FRISTA_EXECUTABLE"]
    FRISTA_USERNAME = settings["FRISTA_USERNAME"]
    FRISTA_PASSWORD = settings["FRISTA_PASSWORD"]
    FRISTA_LOGIN_DELAY_SECONDS = float(settings["FRISTA_LOGIN_DELAY_SECONDS"])
    FRISTA_STANDBY_SECONDS = float(settings["FRISTA_STANDBY_SECONDS"])


_apply_settings(_load_user_settings())
