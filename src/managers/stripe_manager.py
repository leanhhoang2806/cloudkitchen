import stripe
from src.managers.configuration_manager import CONFIG
from src.errors.custom_exceptions import GenericTryError
from src.models.data_model import StripeClientSecret
from src.managers.dish_manager import DishManager
from uuid import UUID
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


stripe.api_key = CONFIG.STRIPE_API_KEY
dish_manager = DishManager()


class StripeManager:

    def create_intent(self, dish_ids: List[UUID]) -> StripeClientSecret:
        try:
            dishes = dish_manager.get_dishes_by_ids(dish_ids)
            total = int(sum([dish.price for dish in dishes]) * 100)
            intent = stripe.PaymentIntent.create(amount=total, currency="usd")
            return StripeClientSecret(client_secret=intent["client_secret"])
        except Exception:
            raise GenericTryError
