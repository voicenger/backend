import json
from datetime import datetime, timedelta

from decouple import config
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.dateparse import parse_date
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Chat, Message, UserChat
from .serializers import ChatSerializer, MessageSerializer, UserChatSerializer, RegisterSerializer


# Create your views here.

def index(request):
    return render(request,'index.html')



def profile(request):
    user=request.user

    auth0_user=user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'name':user.first_name,
        'picture':auth0_user.extra_data['picture']
    }

    context={
        'user_data':json.dumps(user_data,indent=4),
        'auth0_user':auth0_user
    }


    return render(request,'profile.html',context)

#logout
# https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}

def logout(request):
    django_logout(request)

    domain=config('APP_DOMAIN')
    client_id=config('APP_CLIENT_ID')
    return_to='http://127.0.0.1:8000/api/app/'

    return HttpResponseRedirect(f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}")


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
