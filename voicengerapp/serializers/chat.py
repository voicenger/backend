from rest_framework import serializers
from ..models import Chat, ChatParticipant

# Сериализатор для чатов
class ChatSerializer(serializers.ModelSerializer):
    def validat_closed_at(self, value):
        if value and value < self.instance.created_at:
            raise serializers.ValidationError("The closing date cannot be earlier than the chat creation date.")
        return value
    class Meta:
        model = Chat
        fields = '__all__'

# Сериализатор для участников чатов
class ChatParticipantSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if ChatParticipant.objects.filter(user=data['user'], chat=data['chat']).exists():
            raise serializers.ValidationError("The user is already a member of this chat room.")
        return data
    class Meta:
        model = ChatParticipant
        fields = '__all__'
