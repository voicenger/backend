from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer
from ..models import User

# ViewSet для пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Представление для регистрации
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Представление для обновления профиля
class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
