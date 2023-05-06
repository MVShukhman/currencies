from sqlalchemy import Column, String, Float
from app.db.connection import Base


class ExchangeRate(Base):
    __tablename__ = "rates"

    currency = Column(String, primary_key=True)
    rate = Column(Float, nullable=False)
