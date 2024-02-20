import logging
import jwt
from src.managers.configuration_manager import CONFIG
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JsonWebToken:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    def __init__(self):
        self.auth0_issuer_url = CONFIG.AUTH0_ISSUER
        self.auth0_audience = CONFIG.API_IDENTIFIER
        self.algorithm = "RS256"
        self.jwks_uri = f"{self.auth0_issuer_url}.well-known/jwks.json"

    def validate(self, jwt_access_token):
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(jwt_access_token).key
            payload = jwt.decode(
                jwt_access_token,
                jwt_signing_key,
                algorithms=self.algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
                leeway=300,  # 5 minutes leeway (adjust as needed)
            )
            return payload
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise HTTPException(status_code=401, detail="Failed validation")
