import logging

from rest_framework import serializers
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', 'profile_pictures', 'date_of_birth', 'facebook_profile', 'notifications_enabled', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            profile_pictures=validated_data.get('profile_pictures', None),
            date_of_birth=validated_data.get('date_of_birth', None),
            facebook_profile=validated_data.get('facebook_profile', ''),
            notifications_enabled=validated_data.get('notifications_enabled', True),
        )
        user.set_password(validated_data['password'])
        logger.debug(f"Creating user: {user.username} with hashed password: {user.password}")
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        logger.debug(f"Validating user: {username} with password: {password}")

        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    if not user.is_active:
                        logger.debug(f"User {username} is inactive.")
                        raise serializers.ValidationError("User is inactive.")
                    logger.debug(f"User {username} authenticated successfully.")
                    return {"username": user.username}
                else:
                    logger.debug(f"Password is incorrect for user: {username}")
                    raise serializers.ValidationError("Invalid credentials.")
            except User.DoesNotExist:
                logger.debug(f"User {username} does not exist.")
                raise serializers.ValidationError("Invalid credentials.")
        logger.debug("Username and password must be provided.")
        raise serializers.ValidationError("Must include 'username' and 'password'.")

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatParticipant
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageReadReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReadReceipt
        fields = '__all__'
