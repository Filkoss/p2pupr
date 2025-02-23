import os
from dotenv import load_dotenv

# Načte proměnné z .env souboru
load_dotenv()

# Síťová konfigurace
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 65530))
TIMEOUT = int(os.getenv("TIMEOUT", 5))

# Konfigurace MySQL databáze
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "Banka")
