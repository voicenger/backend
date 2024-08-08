from rest_framework import serializers
from ..models import Chat, ChatParticipant

# Сериализатор для чатов
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

# Сериализатор для участников чатов
class ChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatParticipant
        fields = '__all__'
