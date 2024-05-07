from src.managers.ops_manager import OpsManager
from src.routes.custom_api_router import CustomAPIRouter
from src.models.postgres_model import SellerApplicationPydantic
from src.models.data_model import UpdateSellerApplication
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging


router = CustomAPIRouter()
ops_manager = OpsManager()
ops_api_key = os.environ.get("OPS_ACCESS_KEY")

security = HTTPBearer()


async def validate_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    ops_api_key = os.environ.get("OPS_ACCESS_KEY")
    if token != ops_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/ops/seller-application/all")
async def get_all_seller_application(current_user=Depends(validate_current_user)):
    applications = ops_manager.get_all_seller_application()
    logging.error(applications)
    return [
        SellerApplicationPydantic.from_orm(application) for application in applications
    ]


@router.put("/ops/seller-application")
async def update_seller_application(
    update_data: UpdateSellerApplication, current_user=Depends(validate_current_user)
):
    application = ops_manager.update_seller_application(
        update_data.application_id, update_data.status
    )
    return SellerApplicationPydantic.from_orm(application)
