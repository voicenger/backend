import json
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey


class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        """
        Initializes the Auth0 JWT Bearer Token Validator.

        Args:
            domain (str): The Auth0 domain.
            audience (str): The expected audience (client ID) for the JWT token.

        Sets up the public key from Auth0's JWKS endpoint and configures the claims options.
        """
        issuer = f"https://{domain}/"
        
        # Fetches the public keys from Auth0's JWKS endpoint
        jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        
        # Initializes the base JWTBearerTokenValidator with the public key
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        
        # Configures the claims that are required and their expected values
        self.claims_options = {
            "exp": {"essential": True},  # Token expiration time must be present
            "aud": {"essential": True, "value": audience},  # Token audience must match the expected audience
            "iss": {"essential": True, "value": issuer},  # Token issuer must match the expected issuer
        }