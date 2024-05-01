from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.managers.configuration_manager import CONFIG
from functools import wraps


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )

    def get_session(self) -> Session:
        db = self.SessionLocal()
        try:
            return db
        finally:
            db.close()


db = Database(CONFIG.POSTGRES_DATABASE_URL_CONNECTION_STRING)
session = db.get_session()


def provide_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            session = db.get_session()
            # Call the function with the session as an argument
            result = func(*args, session, **kwargs)

            return result
        except Exception as e:
            # Rollback the session if an exception occurs
            session.rollback()
            # Optionally, handle or log the exception
            raise e
        finally:
            # Close the session when done
            session.close()

    return wrapper
