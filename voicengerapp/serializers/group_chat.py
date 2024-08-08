from rest_framework import serializers
from ..models import GroupChat, GroupChatParticipant, GroupChatFile, GroupChatLink

# Сериализатор для групповых чатов
class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'

# Сериализатор для участников групповых чатов
class GroupChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatParticipant
        fields = '__all__'

# Сериализатор для файлов групповых чатов
class GroupChatFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatFile
        fields = '__all__'

# Сериализатор для ссылок на групповые чаты
class GroupChatLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatLink
        fields = '__all__'
