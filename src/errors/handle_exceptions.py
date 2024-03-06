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
            exception_map = set(
                [
                    InvalidTokenException,
                    UniqueViolationException,
                    MediaUploadLimitException,
                ]
            )

            for exception in exception_map:
                if isinstance(e, exception):
                    raise HTTPException(status_code=400, detail=e.message)

            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
