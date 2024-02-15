from functools import wraps


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Handle exception (e.g., log error)
            print(f"An error occurred: {str(e)}")
            raise e

    return wrapper
