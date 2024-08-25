import requests
from jose import jwt
from jose.exceptions import JWTError

from django.conf import settings

from voicengerapp.models import User

def get_jwk_key(token):
    """
    Retrieves the RSA key used to sign the JWT token from Auth0's JWKs endpoint.

    Args:
        token (str): The JWT token from which to extract the key.

    Returns:
        dict: The RSA key used to sign the JWT token.

    Raises:
        JWTError: If the RSA key cannot be found in the JWKs.
    """
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    unverified_header = jwt.get_unverified_header(token)
    
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break

    if rsa_key:
        return rsa_key
    else:
        raise JWTError("RSA key not found")

def save_user_to_db(id_token):
    """
    Decodes the JWT token, verifies it, and saves the user information to the database.

    Args:
        id_token (str): The JWT token provided by Auth0.

    Returns:
        User: The Django User object created or retrieved from the database.

    Raises:
        ValueError: If token verification fails or if any error occurs during decoding.
    """
    try:
        # Retrieve the RSA key for verifying the JWT token
        rsa_key = get_jwk_key(id_token)
        
        # Decode and verify the JWT token
        payload = jwt.decode(
            id_token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.SOCIAL_AUTH_AUTH0_KEY,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )
    except JWTError as e:
        raise ValueError(f"Token verification failed: {e}")

    user_id = payload.get('sub')
    email = payload.get("email")
    username = payload.get("nickname", email.split('@')[0])
    
    # Create or retrieve the user based on the username and email
    user, created = User.objects.get_or_create(
        auth0_sub=user_id,
        defaults={'username': username, 'email': email}
    )
    return user

def decode_and_verify_token(token):
    """
    Decodes and verifies a JWT token without saving the user in the database.

    Args:
        token (str): JWT token provided by Auth0.

    Returns:
        dict: Decoded payload from the JWT token.

    Raises:
        ValueError: If token verification fails or an error occurs during decoding.
    """
    try:
        # Retrieve RSA key for verifying the JWT token
        rsa_key = get_jwk_key(token)
        
        # Decode and verify the JWT token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.API_IDENTIFIER,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )
        return payload
    except JWTError as e:
        raise ValueError(f"Token verification failed: {e}")
