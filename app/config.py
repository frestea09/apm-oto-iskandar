"""Central configuration for database and BPJS automation."""

DB_CONFIG = {
    "host": "172.168.1.2",
    "user": "root",
    "password": "s1mrs234@",
    "database": "otista_dev",
    "port": 3306,
    # Pastikan menggunakan plugin autentikasi bawaan yang didukung pyinstaller
    "auth_plugin": "mysql_native_password",
}

BPJS_EXECUTABLE = r"C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe"
BPJS_USERNAME = "1002r006th"
BPJS_PASSWORD = "#Bandung28"
LOGIN_DELAY_SECONDS = 0.8
POST_LOGIN_DELAY_SECONDS = 0.6
FORM_FILL_DELAY_SECONDS = 2.5

# External system launch configuration
CHROME_EXECUTABLE = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
CHECKIN_URL = "http://172.168.1.175:8070"
