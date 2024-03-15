from fastapi import Depends, status
from src.validations.validators import validate_token
from src.routes.custom_api_router import CustomAPIRouter
from src.managers.payment_manager import PaymentManager
from src.managers.stripe_manager import StripeManager
from src.models.data_model import (
    StripeClientSecret,
    StripePaymentInfo,
    PaymentUpdate,
    EmailOnlyPayload,
)
from src.errors.custom_exceptions import SellerSubscriptionNotActive

router = CustomAPIRouter()
stripe_manager = StripeManager()
payment_manager = PaymentManager()


@router.post("/stripe-payment/", response_model=StripeClientSecret)
async def payment_amount(
    dish_ids: StripePaymentInfo,
    token=Depends(validate_token),
):
    return stripe_manager.create_intent(dish_ids.dish_ids)


@router.put("/stripe-payment/update-limit")
async def upddate_payment(
    generic_payload: EmailOnlyPayload, token=Depends(validate_token)
):
    if not stripe_manager.is_seller_subsciption_active(generic_payload.email):
        raise SellerSubscriptionNotActive

    payment_manager.payment_update_by_email(
        PaymentUpdate(
            email=generic_payload.email,
            picture_upload_limit=10,
            dishes_to_feature_limit=5,
        )
    )

    return status.HTTP_202_ACCEPTED
