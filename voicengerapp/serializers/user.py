from rest_framework import serializers
from ..models import User
from datetime import datetime

# Сериализатор для пользователей
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_date_of_birth(self, value):
        if value and value.date() > datetime.now().date():
            raise serializers.ValidationError("The date of birth cannot be in the future.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exist.")
        return value

    def validate_bio(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Bio cannot be longer than 500 characters.")
        return value