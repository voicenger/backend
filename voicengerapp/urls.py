from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ChatViewSet, MessageViewSet, UserChatViewSet, RegisterView, logout, auth0_callback, login_redirect

router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'userchats', UserChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('app/',include('social_django.urls')),
    path('app/logout/',logout,name='logout'),
    path('messages/chat/<int:id>/', MessageViewSet.as_view({'get': 'user_chat_messages'}), name='user_chat_messages'),
    path('login/', login_redirect, name='login_redirect'),
    path('logout/', logout, name='logout'),
    path('callback/', auth0_callback, name='auth0_callback')
]
