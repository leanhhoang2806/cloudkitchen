from fastapi import Depends
from src.validations.validators import validate_token
from src.routes.custom_api_router import CustomAPIRouter
from src.managers.stripe_manager import StripeManager
from src.models.data_model import StripeClientSecret, StripePaymentInfo

router = CustomAPIRouter()
stripe_manager = StripeManager()


@router.post("/stripe-payment/", response_model=StripeClientSecret)
async def payment_amount(
    dish_ids: StripePaymentInfo,
    token=Depends(validate_token),
):
    return stripe_manager.create_intent(dish_ids.dish_ids)
