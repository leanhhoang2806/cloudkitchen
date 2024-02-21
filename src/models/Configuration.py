from pydantic import BaseModel


class Configuration(BaseModel):
    AUTH0_ISSUER: str
    API_IDENTIFIER: str
    POSTGRES_DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
