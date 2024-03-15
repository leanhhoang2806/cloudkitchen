import stripe
from src.managers.configuration_manager import CONFIG
from src.errors.custom_exceptions import GenericTryError
from src.models.data_model import StripeClientSecret
from src.managers.dish_manager import DishManager
from uuid import UUID
from typing import List
from src.errors.custom_exceptions import (
    MultipleSellerSubscriptionDetected,
    ValidateSellerSubsciprtionError,
)
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

    def is_seller_subsciption_active(self, customer_email: str) -> bool:
        try:
            customer = stripe.Customer.list(email=customer_email)
            if len(customer) > 1:
                raise MultipleSellerSubscriptionDetected
            customer_id = customer.data[0].id
            subscriptions = stripe.Subscription.list(customer=customer_id)
            active_subscription = [
                sub for sub in subscriptions.data if sub.status == "active"
            ]
            return len(active_subscription) > 0

        except Exception:
            raise ValidateSellerSubsciprtionError
