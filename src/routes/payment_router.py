from fastapi import Depends
from src.validations.validators import validate_token
from src.managers.payment_manager import PaymentManager
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from src.models.postgres_model import PaymentPydantic
from src.models.data_model import PaymentUpdate, PaymentCreate

router = CustomAPIRouter()
payment_manager = PaymentManager()


@router.get("/payment/{payment_id}", response_model=PaymentPydantic)
async def get_payment(payment_id: UUID, token=Depends(validate_token)):
    payment = payment_manager.get(payment_id)
    return PaymentPydantic.from_orm(payment)


@router.post("/payment/", response_model=PaymentPydantic)
async def create_payment(payment_data: PaymentCreate, token=Depends(validate_token)):
    payment = payment_manager.create(payment_data)
    return PaymentPydantic.from_orm(payment)


@router.put("/payment/{payment_id}", response_model=PaymentPydantic)
async def update_payment(
    payment_id: UUID, payment_data: PaymentUpdate, token=Depends(validate_token)
):
    payment = payment_manager.update(payment_id, payment_data)
    return PaymentPydantic.from_orm(payment)


@router.delete("/payment/{payment_id}")
async def delete_payment(payment_id: UUID, token=Depends(validate_token)):
    deleted_count = payment_manager.delete(payment_id)
    return {"deleted_count": deleted_count}
