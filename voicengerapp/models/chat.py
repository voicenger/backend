from django.db import models
from .user import User

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
