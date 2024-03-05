from functools import wraps
from fastapi import HTTPException
from src.errors.custom_exceptions import (
    InvalidTokenException,
    UniqueViolationException,
    MediaUploadLimitException,
)
import logging


logging.basicConfig(level=logging.INFO)


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            exception_map = {
                InvalidTokenException: {"status_code": 401, "detail": "Invalid token"},
                UniqueViolationException: {
                    "status_code": 400,
                    "detail": str(e),
                },  # Convert e.message to str(e)
                MediaUploadLimitException: {
                    "status_code": 400,
                    "detail": str(e),
                },  # Convert e.message to str(e)
            }

            for exception_type, response_data in exception_map.items():
                if isinstance(e, exception_type):
                    raise HTTPException(**response_data)

            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
