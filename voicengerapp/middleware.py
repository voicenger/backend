from django.utils.deprecation import MiddlewareMixin

class Auth0TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            access_token = request.session.get('access_token')
            refresh_token = request.session.get('refresh_token')

            if access_token and refresh_token:
                request.access_token = access_token
                request.refresh_token = refresh_token
            else:
                request.access_token = None
                request.refresh_token = None
        else:
            request.access_token = None
            request.refresh_token = None