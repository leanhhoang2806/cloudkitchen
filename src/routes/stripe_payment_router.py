from fastapi import Depends, status, Request
from fastapi.responses import JSONResponse
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
from src.models.data_model import StripeSubscriptionStatus
import stripe
from src.managers.configuration_manager import CONFIG
import json

stripe.api_key = CONFIG.STRIPE_API_KEY
router = CustomAPIRouter()
stripe_manager = StripeManager()
payment_manager = PaymentManager()


@router.post("/stripe-payment/", response_model=StripeClientSecret)
async def payment_amount(
    payment_info: StripePaymentInfo,
    token=Depends(validate_token),
):
    return stripe_manager.create_intent(payment_info.buyer_id, payment_info.dish_ids)


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


@router.get("/stripe-payment/", response_model=StripeSubscriptionStatus)
async def get_subscription_status(
    email: EmailOnlyPayload, token=Depends(validate_token)
):
    status = stripe_manager.is_seller_subsciption_active(email.email)
    return StripeSubscriptionStatus(active_status=status)


@router.post("/stripe-payment/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError:
        return status.HTTP_400_BAD_REQUEST

    if event["type"] == "customer.subscription.deleted":

        # change update user limit to 3
        subscription = event["data"]["object"]
        customer_id = subscription["customer"]
        stripe_manager.on_subsciprtion_cancel(customer_id)

        return JSONResponse(
            status_code=200, content={"message": "Subscription cancellation received"}
        )

    # Handle other event types if needed

    return JSONResponse(status_code=200)
