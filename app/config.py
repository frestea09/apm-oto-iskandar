"""Central configuration for database and BPJS automation."""
import os

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

BPJS_EXECUTABLE = r"C:\Program Files (x86)\BPJS Kesehatan\Aplikasi Sidik Jari BPJS Kesehatan\After.exe"
BPJS_USERNAME = "1002r006th"
BPJS_PASSWORD = "#Bandung28"
LOGIN_DELAY_SECONDS = 0.8
POST_LOGIN_DELAY_SECONDS = 0.6
FORM_FILL_DELAY_SECONDS = 2.5

# External system launch configuration
CHROME_EXECUTABLE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHECKIN_URL = "http://172.168.1.175:8070"
FRISTA_EXECUTABLE = r"C:\Users\ilman\Documents\Frista\Frista.exe"
FRISTA_USERNAME = BPJS_USERNAME
FRISTA_PASSWORD = BPJS_PASSWORD
FRISTA_LOGIN_DELAY_SECONDS = 1.2
