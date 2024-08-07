# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    notifications_enabled = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='voicengerapp_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='voicengerapp_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Chat(models.Model):
    chat_image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    closed_at = models.DateTimeField(blank=True, null=True)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, related_name='chats')

class ChatParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'chat')

class Message(models.Model):
    MESSAGE_TYPES = (
        ('Text', 'Text'),
        ('Audio', 'Audio'),
        ('Video', 'Video')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPES)
    content = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='audio_files/', blank=True, null=True)
    video_file = models.FileField(upload_to='video_files/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)

class MessageReadReceipt(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    chat_participant = models.ForeignKey(ChatParticipant, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

class GroupChat(Chat):
    group_name = models.CharField(max_length=100)
    group_image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    is_public = models.BooleanField(default=False)
    rules = models.TextField(blank=True)
    invite_link = models.URLField(blank=True, null=True)

class GroupChatParticipant(ChatParticipant):
    is_muted = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

class GroupChatFile(models.Model):
    FILE_TYPES = (
        ('Document', 'Document'),
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Audio', 'Audio')
    )
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=50, choices=FILE_TYPES)
    file = models.FileField(upload_to='group_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

class GroupChatLink(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
