from sqlalchemy.orm import Session
from app.services.currency import CurrencyService
from app.db.connection import get_db
from fastapi import Depends


def get_currency_service(db: Session = Depends(get_db)) -> CurrencyService:
    return CurrencyService(db)
