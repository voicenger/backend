from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Chat, Message, UserChat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at', 'updated_at']

    def validate_participants(self, participants):
        if len(participants) == 2:
            raise serializers.ValidationError("A chat should have exactly two participants")
        return participants

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['participants'] = [{'id': p.id, 'username': p.username} for p in instance.participants.all()]
        return representation


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_username', 'text', 'timestamp', 'is_read']
        read_only_fields = ['sender']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['sender'] = user
        return super(MessageSerializer, self).create(validated_data)

    def validate(self, data):
        chat = data.get('chat', None)
        sender = data.get('sender', None)

        if chat and sender and sender not in chat.participants:
            raise serializers.ValidationError("The sender is not a participant of the chat.")

        return data


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ['user', 'chat', 'last_read_message']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'min_length': 4},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user
