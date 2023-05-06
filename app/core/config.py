import os

API_KEY = ""
API_URL = "https://api.apilayer.com/exchangerates_data/latest?symbols=&base=USD"

DB_NAME = os.environ.get("DB_NAME", "currency_db")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
