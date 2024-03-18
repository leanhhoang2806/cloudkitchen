import stripe
from src.managers.configuration_manager import CONFIG
from src.errors.custom_exceptions import (
    GenericTryError,
    ReduceLimitOnSubscriptionCancelledError,
)
from src.models.data_model import StripeClientSecret, PaymentUpdate
from src.managers.dish_manager import DishManager
from src.managers.payment_manager import PaymentManager
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
payment_manager = PaymentManager()


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

    def on_subsciprtion_cancel(self, stripe_customer_id: str) -> None:
        try:
            customer = stripe.Customer.list(customer_id=stripe_customer_id)
            if len(customer) > 1:
                raise MultipleSellerSubscriptionDetected
            customer_email = customer.data[0].email
            payment_manager.payment_update_by_email(
                PaymentUpdate(
                    email=customer_email,
                    picture_upload_limit=1,
                    dishes_to_feature_limit=1,
                )
            )

            return
        except Exception:
            raise ReduceLimitOnSubscriptionCancelledError
