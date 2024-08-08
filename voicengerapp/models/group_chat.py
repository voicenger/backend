from django.db import models
from .chat import Chat, ChatParticipant
from .user import User

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
