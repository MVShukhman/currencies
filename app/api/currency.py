import http

from fastapi import APIRouter, Depends, HTTPException
from app.deps.deps import get_currency_service
from app.schemas.currency import CurrencyRequest, CurrencyResponse
from app.services.currency import (
    CurrencyService,
    CurrencyNotExistsError,
    NotUpdatedRatesError,
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/refresh_rates")
def update_currency_rates(
    currency_service: CurrencyService = Depends(get_currency_service),
):
    logger.info("Updating currency rates...")
    try:
        currency_service.update_rates()
    except NotUpdatedRatesError:
        logger.error("Rates were not updated")
        raise HTTPException(status_code=http.HTTPStatus.SERVICE_UNAVAILABLE)
    return {"status": "success"}


@router.get("/api/calculate_exchange", response_model=CurrencyResponse)
def calculate_exchange_data(
    currency_from: str,
    currency_to: str,
    value: float,
    currency_service: CurrencyService = Depends(get_currency_service),
):
    try:
        result = currency_service.calc_exchange(currency_from, currency_to, value)
    except CurrencyNotExistsError as error:
        raise HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND,
            detail=f"Currency {error.currency} was not found",
        )

    response = CurrencyResponse(
        currency_from=currency_from, currency_to=currency_to, value=value, result=result
    )
    return response
