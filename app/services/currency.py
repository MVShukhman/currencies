import http

from sqlalchemy.orm import Session
from app.db.models import ExchangeRate
from app.core.config import API_URL, API_KEY
import json
import requests

import logging

logger = logging.getLogger(__name__)


class CurrencyNotExistsError(Exception):
    def __init__(self, currency: str) -> None:
        super().__init__()
        self.currency = currency


class NotUpdatedRatesError(Exception):
    pass


def request_rates_with_retries(retries: int = 3) -> dict:
    headers = {"apikey": API_KEY}
    for i in range(retries):
        logger.info("Requesting exchange data from external API")
        response = requests.request("GET", API_URL, headers=headers)
        if response.status_code == http.HTTPStatus.OK:
            logger.info("Request was successful, got new rates")
            data = json.loads(response.content)
            return data["rates"]
        logger.error("Error getting exchange data")
    return {}


class CurrencyService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _insert_with_update(self, data: dict):
        for currency, rate in data.items():
            current_rate = (
                self.db.query(ExchangeRate)
                .filter(ExchangeRate.currency == currency)
                .one_or_none()
            )

            if current_rate is None:
                current_rate = ExchangeRate(currency=currency, rate=rate)
                self.db.add(current_rate)
                logger.info(f"New currency {current_rate.currency} was added")

            else:
                current_rate.rate = rate

        self.db.commit()

    def _get_rate(self, currency: str) -> float:
        rate = (
            self.db.query(ExchangeRate.rate)
            .filter(ExchangeRate.currency == currency)
            .first()
        )

        if not rate:
            raise CurrencyNotExistsError(currency=currency)

        return rate[0]

    def update_rates(self) -> None:
        logger.info("Updating existing rates")
        new_rates = request_rates_with_retries()
        if new_rates is None:
            raise NotUpdatedRatesError
        self._insert_with_update(new_rates)
        logger.info("Rates were updated successfully")

    def calc_exchange(
        self, from_currency: str, to_currency: str, value: float
    ) -> float:
        from_rate = self._get_rate(from_currency)
        to_rate = self._get_rate(to_currency)
        return value * to_rate / from_rate
