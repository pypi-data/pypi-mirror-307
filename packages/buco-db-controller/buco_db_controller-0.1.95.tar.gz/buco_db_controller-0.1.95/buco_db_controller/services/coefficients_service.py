import logging
from typing import Optional

from buco_db_controller.models.coefficients import Coefficients
from buco_db_controller.repositories.coefficients_repository import CoefficientsRepository
from buco_db_controller.utils import mappers

LOGGER = logging.getLogger(__name__)


class CoefficientsService:
    def __init__(self):
        self.coefficients_repository = CoefficientsRepository()

    def insert_coefficients(self, coefficients):
        self.coefficients_repository.insert_coefficients(coefficients)
        LOGGER.info('Inserted coefficients data')

    def upsert_many_coefficients(self, coefficients):
        self.coefficients_repository.upsert_many_coefficients(coefficients)
        LOGGER.info('Upsert coefficients data')

    def get_coefficients(self, season: int) -> Optional[dict]:
        response = self.coefficients_repository.get_coefficients(season)

        if not response.get('data', []):
            return None

        coefficients = Coefficients.from_dict(response)
        return coefficients

    def get_country_coefficient(self, country: str, season: int) -> Optional[dict]:
        response = self.coefficients_repository.get_coefficients(season)

        if not response.get('data', []):
            return None

        uefa_ranking = Coefficients.from_dict(response)
        country = mappers.find_fuzzy_item(country, uefa_ranking.coefficients.keys())
        coefficient = next((coefficient for key, coefficient in uefa_ranking.coefficients.items() if key == country), None)
        return coefficient
