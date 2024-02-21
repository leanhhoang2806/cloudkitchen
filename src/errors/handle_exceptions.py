from functools import wraps
from fastapi import HTTPException
from src.errors.custom_exceptions import InvalidTokenException
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            if isinstance(e, InvalidTokenException):
                raise HTTPException(status_code=401, detail="Invalid token")
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
