from datetime import datetime, timedelta
from django.contrib.auth import logout as django_logout
from django.utils.dateparse import parse_date
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Chat, Message, UserChat
from .serializers import ChatSerializer, MessageSerializer, UserChatSerializer, RegisterSerializer
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login, logout as django_logout
import requests
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from .utils import save_user_to_db # Function for saving user


def login_redirect(request):
    # URL for redirecting to the Auth0 login page with required query parameters
    auth0_url = (
        f"https://{settings.AUTH0_DOMAIN}/authorize?"
        f"audience={settings.API_IDENTIFIER}&"  # API audience to which the access token should be valid
        f"response_type=code&"  # Authorization code flow
        f"client_id={settings.SOCIAL_AUTH_AUTH0_KEY}&"  # Client ID for the Auth0 application
        f"redirect_uri={settings.AUTH0_CALLBACK_URL}&"  # URI to which Auth0 will redirect after login
        f"scope=openid profile email"  # Scopes to request from Auth0
    )
    return redirect(auth0_url)

def auth0_callback(request):
    code = request.GET.get('code')

    if not code:
        # Handle the case where the authorization code is missing from the request
        return HttpResponseBadRequest("Authorization code is missing.")

    try:
        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.SOCIAL_AUTH_AUTH0_KEY,
            'client_secret': settings.SOCIAL_AUTH_AUTH0_SECRET,
            'code': code,
            'redirect_uri': settings.AUTH0_CALLBACK_URL,
        }
        token_headers = {'Content-Type': 'application/json'}
        token_response = requests.post(token_url, json=token_data, headers=token_headers)

        if token_response.status_code != 200:
            # Handle token request errors
            return HttpResponseServerError(f"Failed to get tokens: {token_response.text}")

        tokens = token_response.json()
        id_token = tokens.get('id_token')
        access_token = tokens.get('access_token')

        if not id_token or not access_token:
            # Handle the case where tokens are missing
            return HttpResponseServerError("Failed to retrieve tokens from response.")

        # Save the user and handle login
        user = save_user_to_db(id_token)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Save the access token in an HttpOnly cookie for security
        response = HttpResponse('Authentication successful')
        response.set_cookie('access_token', access_token, httponly=True, secure=True)
        
        return response

    except requests.RequestException as e:
        # Handle network-related errors
        return HttpResponseServerError(f"Network error occurred: {str(e)}")

    except ValueError as e:
        # Handle errors related to token processing
        return HttpResponseServerError(f"Token error: {str(e)}")

    except Exception as e:
        # Handle any other unexpected errors
        return HttpResponseServerError(f"An unexpected error occurred: {str(e)}")

def logout(request):
    # End the user's session in Django
    django_logout(request)
    
    # Create a response and redirect to Auth0 logout URL
    # Also remove the access_token from Cookies
    response = redirect(f"https://{settings.AUTH0_DOMAIN}/v2/logout?client_id={settings.SOCIAL_AUTH_AUTH0_KEY}&returnTo={settings.LOGOUT_REDIRECT_URL}")
    response.delete_cookie('access_token')
    
    return response


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Chat.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You must be authenticated to view this content.")

        return Chat.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def parse_custom_date(self, date_str):
        if date_str == "yesterday":
            return (datetime.today() - timedelta(days=1)).date()
        elif date_str == "day_before_yesterday":
            return (datetime.today() - timedelta(days=2)).date()
        elif date_str == "last_7_days":
            return (datetime.today() - timedelta(days=7)).date()
        else:
            return parse_date(date_str)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('date_from', openapi.IN_QUERY,
                              description="Start date (YYYYY-MM-DD) or yesterday, day_before_yesterday, last_7_days",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('date_to', openapi.IN_QUERY, description="End date (YYYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('last', openapi.IN_QUERY, description="Last N messages", type=openapi.TYPE_INTEGER),
        ]
    )
    def user_chat_messages(self, request, id=None):
        chat_id = id
        messages = Message.objects.filter(chat_id=chat_id)

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        last = request.query_params.get('last')

        if date_from:
            date_from = self.parse_custom_date(date_from)
            if date_from:
                messages = messages.filter(timestamp__date__gte=date_from)

        if date_to:
            date_to = parse_date(date_to)
            if date_to:
                messages = messages.filter(timestamp__date__lte=date_to)

        if last and last.isdigit():
            messages = messages.order_by('-timestamp')[:int(last)]

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserChat.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You must be authenticated to view this content.")

        return UserChat.objects.filter(user=user)


class RegisterView(generics.CreateAPIView):
    queryset = UserChat.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
