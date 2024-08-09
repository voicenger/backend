from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer
from ..models import User


# ViewSet для пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        # Для создания пользователя использовать RegisterSerializer
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        # Разрешаем всем создавать пользователя (регистрацию)
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


# Представление для обновления профиля
class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
