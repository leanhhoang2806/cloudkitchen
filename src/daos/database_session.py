from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.managers.configuration_manager import CONFIG


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self) -> Session:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


db = Database(CONFIG.POSTGRES_DATABASE_URL)
session = db.get_session()
