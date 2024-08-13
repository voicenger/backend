import requests
from django.conf import settings
from rest_framework import authentication, exceptions
from jose import JWTError, jwt
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')
            
            payload = self.decode_jwt(token)
            user_id = payload.get('sub')
            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid token')

            # Проверьте, что используете правильный метод поиска пользователя
            try:
                user = User.objects.get(username=user_id)  # Замените на правильное поле
            except User.DoesNotExist:
                # Логика создания пользователя, если необходимо
                user = User.objects.create_user(
                    username=user_id,
                    password='temporary_password',  # Используйте другой метод для создания пароля
                )

            return (user, token)

        except JWTError as e:
            raise exceptions.AuthenticationFailed('Invalid token') from e
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token header')

    def decode_jwt(self, token):
        try:
            jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
            response = requests.get(jwks_url)
            jwks = response.json()

            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
                    break

            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=['RS256'],
                    audience=settings.JWT_AUDIENCE,
                    issuer=settings.JWT_ISSUER
                )
                return payload
            else:
                raise exceptions.AuthenticationFailed('Unable to find appropriate key')

        except JWTError:
            raise exceptions.AuthenticationFailed('Invalid token')
