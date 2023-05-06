import logging
from fastapi import FastAPI
from app.api import currency
from app.db.connection import Base, engine
from app.db.models import ExchangeRate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(currency.router)
