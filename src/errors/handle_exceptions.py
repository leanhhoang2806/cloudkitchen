from functools import wraps
from fastapi import HTTPException
from src.errors.custom_exceptions import InvalidTokenException, UniqueViolationException
import logging


logging.basicConfig(level=logging.INFO)


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            if isinstance(e, InvalidTokenException):
                raise HTTPException(status_code=401, detail="Invalid token")
            if isinstance(e, UniqueViolationException):
                raise HTTPException(
                    status_code=400, detail="Unique Constraint Violation"
                )
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
