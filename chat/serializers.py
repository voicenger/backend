from rest_framework import serializers
from .models import GroupChat, GroupChatParticipant, GroupChatFile, GroupChatLink


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
