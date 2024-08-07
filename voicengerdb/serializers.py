from rest_framework import serializers
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt


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
        user.save()
        return user

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
