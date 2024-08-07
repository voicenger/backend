from rest_framework import serializers
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt, GroupChat, GroupChatParticipant, GroupChatFile, GroupChatLink

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

class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'

class GroupChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatParticipant
        fields = '__all__'

class GroupChatFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatFile
        fields = '__all__'

class GroupChatLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatLink
        fields = '__all__'
