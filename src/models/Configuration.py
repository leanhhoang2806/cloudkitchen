from pydantic import BaseModel


class Configuration(BaseModel):
    AUTH0_ISSUER: str
    API_IDENTIFIER: str
    POSTGRES_DATABASE_URL: str
