from rest_framework import serializers

from .models import Chat, Message, UserChat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_username', 'text', 'timestamp', 'is_read']


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ['user', 'chat', 'last_read_message']
