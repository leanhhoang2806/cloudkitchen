import stripe
from src.managers.configuration_manager import CONFIG
from src.errors.custom_exceptions import (
    ReduceLimitOnSubscriptionCancelledError,
)
from src.models.data_model import StripeClientSecret, PaymentUpdate
from uuid import UUID
from typing import List, Union
from src.errors.custom_exceptions import (
    MultipleSellerSubscriptionDetected,
    ValidateSellerSubsciprtionError,
)
import logging
from src.managers.all_managers import ALL_MANAGER
from src.errors.custom_exceptions import BuyerMustUpdateAddressBeforeOrderError
from src.errors.handle_exceptions import handle_errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


stripe.api_key = CONFIG.STRIPE_API_KEY
dish_manager = ALL_MANAGER.dish_manager
payment_manager = ALL_MANAGER.payment_manager
buyer_manager = ALL_MANAGER.buyer_manager
discounted_dish_manager = ALL_MANAGER.discounted_dish_manager


class StripeManager:

    @handle_errors
    def create_intent(
        self, buyer_id: UUID, dish_ids: List[UUID]
    ) -> Union[StripeClientSecret, None]:
        if not buyer_manager.is_address_exist(buyer_id):
            raise BuyerMustUpdateAddressBeforeOrderError
        dishes = dish_manager.get_dishes_by_ids(dish_ids)
        discounts = [
            discounted_dish_manager.get_discounted_dish_by_dish_id(dish.id)
            for dish in dishes
        ]

        matching_dict = {
            discount.dish_id: discount.discounted_percentage
            for discount in discounts
            if discount is not None
        }
        total = 0
        for dish in dishes:
            discounted_percentage = matching_dict.get(dish.id, 0)
            discounted_price = float(dish.price) * (1 - discounted_percentage / 100)

            total += discounted_price
        intent = stripe.PaymentIntent.create(amount=int(total * 100), currency="usd")
        return StripeClientSecret(client_secret=intent["client_secret"])

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
