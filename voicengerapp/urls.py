from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import UserViewSet, ChatViewSet, ChatParticipantViewSet, MessageViewSet, MessageReadReceiptViewSet, GroupChatViewSet, GroupChatParticipantViewSet, GroupChatFileViewSet, GroupChatLinkViewSet, RegisterView, ProfileUpdateView
from rest_framework.permissions import AllowAny

# Создание роутера и регистрация viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'chat-participants', ChatParticipantViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'message-read-receipts', MessageReadReceiptViewSet)
router.register(r'group-chats', GroupChatViewSet)
router.register(r'group-chat-participants', GroupChatParticipantViewSet)
router.register(r'group-chat-files', GroupChatFileViewSet)
router.register(r'group-chat-links', GroupChatLinkViewSet)

# Настройка Schema view для Swagger и ReDoc
schema_view = get_schema_view(
    openapi.Info(
        title="Voicenger API",
        default_version='v1',
        description="API documentation for Voicenger application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@voicenger.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', RegisterView.as_view(), name='users_create'),  # Регистрация пользователя
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('api/profile/', ProfileUpdateView.as_view(), name='profile_update'),  # Обновление профиля
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI
]
