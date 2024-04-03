from pydantic import BaseModel


class Configuration(BaseModel):
    AUTH0_ISSUER: str
    API_IDENTIFIER: str
    POSTGRES_DATABASE_URL_CONNECTION_STRING: str
    S3_ONLY_AWS_ACCESS_KEY_ID: str
    S3_ONLY_AWS_SECRET_ACCESS_KEY: str
    STRIPE_API_KEY: str
    # MONGO_CONNECTION_STRING: str
