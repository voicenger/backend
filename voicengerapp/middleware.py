from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_token = request.session.get('jwt_token')
        if jwt_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {jwt_token}'
