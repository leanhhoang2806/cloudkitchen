from functools import wraps
from fastapi import HTTPException
from src.errors.custom_exceptions import InvalidTokenException


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Log the error
            print(f"An error occurred: {str(e)}")
            # Check if it's an invalid token exception
            if isinstance(e, InvalidTokenException):
                raise HTTPException(status_code=401, detail="Invalid token")
            # If not an invalid token exception, return a generic internal server error message
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
