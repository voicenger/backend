from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Chat, Message, UserChat
from .serializers import ChatSerializer, MessageSerializer, UserChatSerializer, RegisterSerializer

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout as django_logout, get_user_model
from django.http import HttpResponseRedirect
from decouple import config
import json

User = get_user_model()

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

@api_view(['GET'])
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_chats = Chat.objects.filter(participants=user)
    serializer = ChatSerializer(user_chats, many=True)
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
        },
        'chats': serializer.data
    })

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]



class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = UserChat.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
