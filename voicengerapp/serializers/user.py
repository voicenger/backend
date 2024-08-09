from rest_framework import serializers
from ..models import User
from datetime import datetime


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'bio', 'profile_picture', 'date_of_birth', 'facebook_profile']

    def validate(self, data):
        # Проверка совпадения паролей
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Удаляем поле password2, оно не нужно для создания пользователя
        validated_data.pop('password2')
        # Создаем пользователя, используя метод create_user, который хеширует пароль
        user = User.objects.create_user(**validated_data)
        return user

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

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exist.")
        return value