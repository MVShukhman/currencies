from pydantic import BaseModel


class CurrencyItem(BaseModel):
    code: str
    value: float


class CurrencyRequest(BaseModel):
    currency_from: str
    currency_to: str
    value: float


class CurrencyResponse(CurrencyRequest):
    result: float
