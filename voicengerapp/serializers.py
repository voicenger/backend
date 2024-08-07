from rest_framework import serializers
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt, GroupChat, GroupChatParticipant, \
    GroupChatFile, GroupChatLink
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# Сериализатор для регистрации пользователей
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'username', 'password', 'email', 'first_name', 'last_name', 'is_superuser',
            'is_staff', 'is_active', 'bio', 'date_of_birth', 'facebook_profile',
            'notifications_enabled', 'is_admin', 'groups', 'user_permissions'
        )

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_superuser=validated_data.get('is_superuser', False),
            is_staff=validated_data.get('is_staff', False),
            is_active=validated_data.get('is_active', True),
            bio=validated_data.get('bio', ''),
            date_of_birth=validated_data.get('date_of_birth', None),
            facebook_profile=validated_data.get('facebook_profile', ''),
            notifications_enabled=validated_data.get('notifications_enabled', True),
            is_admin=validated_data.get('is_admin', False),
        )

        user.set_password(validated_data['password'])
        user.save()

        # Assign groups and permissions
        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user


# Сериализатор для обновления профиля пользователей
class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


# Сериализатор для пользователей
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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


# Сериализатор для сообщений
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


# Сериализатор для квитанций о прочтении сообщений
class MessageReadReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReadReceipt
        fields = '__all__'


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
