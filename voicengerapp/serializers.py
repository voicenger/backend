
from django.utils import timezone
from rest_framework import serializers

from .models import Chat, Message, User, UserChat, UserProfile


class ChatSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, default=timezone.now)
    updated_at = serializers.DateTimeField(required=False, default=timezone.now)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at', 'updated_at']

    def validate_participants(self, participants):
        if len(participants) != 2:
            raise serializers.ValidationError("A chat must have exactly two participants.")
        return participants

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.name:
            representation['name'] = " & ".join([p.username for p in instance.participants.all()])
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

class WebSocketMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_username', 'text', 'timestamp', 'is_read']
        read_only_fields = ['sender']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sender'] = {
            'id': instance.sender.id,
            'username': instance.sender.username
        }
        return representation

class MessageSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp']
        read_only_fields = ['sender']


class UserChatSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserChat
        fields = ['user', 'username', 'chat', 'last_read_message']
        read_only_fields = ['user']

    def create(self, validated_data):
        if UserChat.objects.filter(chat=validated_data['chat']).count() >= 2:
            raise serializers.ValidationError("This chat already has two participants.")
        return super().create(validated_data)

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'phone_number', 'gender', 'profile_picture']