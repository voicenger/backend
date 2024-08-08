from rest_framework import serializers
from ..models import User

# Сериализатор для пользователей
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
