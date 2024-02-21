from src.models.Configuration import Configuration
import os


class ConfigurationManager:
    def __init__(self) -> None:
        self.configuration = Configuration(
            AUTH0_ISSUER=os.environ.get("AUTH0_ISSUER"),
            API_IDENTIFIER=os.environ.get("API_IDENTIFIER"),
            POSTGRES_DATABASE_URL=os.environ.get("POSTGRES_DATABASE_URL"),
            AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID"),
            AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

    def get_configuration(self) -> Configuration:
        return self.configuration


manager = ConfigurationManager()
CONFIG = manager.get_configuration()
