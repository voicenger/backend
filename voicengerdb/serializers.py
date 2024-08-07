from rest_framework import serializers
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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

