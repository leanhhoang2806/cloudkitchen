from src.models.Configuration import Configuration
import os


class ConfigurationManager:
    def __init__(self) -> None:
        self.configuration = Configuration(
            AUTH0_ISSUER=os.environ.get("AUTH0_ISSUER"),
            API_IDENTIFIER=os.environ.get("API_IDENTIFIER"),
            POSTGRES_DATABASE_URL_CONNECTION_STRING=os.environ.get(
                "POSTGRES_DATABASE_URL_CONNECTION_STRING"
            ),
            S3_ONLY_AWS_ACCESS_KEY_ID=os.environ.get("S3_ONLY_AWS_ACCESS_KEY_ID"),
            S3_ONLY_AWS_SECRET_ACCESS_KEY=os.environ.get(
                "S3_ONLY_AWS_SECRET_ACCESS_KEY"
            ),
            STRIPE_API_KEY=os.environ.get("STRIPE_API_KEY"),
            # MONGO_CONNECTION_STRING=os.environ.get("MONGO_CONNECTION_STRING"),
        )

    def get_configuration(self) -> Configuration:
        return self.configuration


manager = ConfigurationManager()
CONFIG = manager.get_configuration()
