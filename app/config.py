"""Central configuration for database and BPJS automation."""

DB_CONFIG = {
    "host": "172.168.1.2",
    "user": "root",
    "password": "s1mrs234@",
    "database": "otista_dev",
    "port": 3306,
}

BPJS_EXECUTABLE = r"C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe"
BPJS_USERNAME = "1002r006th"
BPJS_PASSWORD = "#Bandung28"
LOGIN_DELAY_SECONDS = 1.2
POST_LOGIN_DELAY_SECONDS = 1.0
FORM_FILL_DELAY_SECONDS = 5
