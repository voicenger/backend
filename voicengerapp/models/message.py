from django.db import models
from .user import User
from .chat import Chat, ChatParticipant

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
