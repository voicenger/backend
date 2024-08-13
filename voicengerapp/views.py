import json

from decouple import config
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated

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

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Message.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You must be authenticated to view this content.")

        user_chats = Chat.objects.filter(participants=user)
        return Message.objects.filter(chat__in=user_chats)


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
