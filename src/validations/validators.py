from fastapi import Depends
from src.validations.jwt_validation import JsonWebToken
import logging
from fastapi.security import OAuth2PasswordBearer

logging.basicConfig(level=logging.INFO)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def validate_token(token: str = Depends(oauth2_scheme)):
    return JsonWebToken().validate(token)
