# chat/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from voicengerdb.models import User


class GroupChat(models.Model):
    group_name = models.CharField(max_length=100)
    group_image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    rules = models.TextField(blank=True, null=True)
    invite_link = models.URLField(blank=True, null=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_in_chats', blank=True)

    def __str__(self):
        return self.group_name

    def add_participant(self, user):
        if self.participants.count() >= 100:
            raise ValidationError("The group chat cannot have more than 100 participants.")
        if self.participants.filter(user=user).exists():
            raise ValidationError("User is already a participant in this group chat.")
        GroupChatParticipant.objects.create(chat=self, user=user)



class GroupChatParticipant(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} in {self.chat.id} (Group)"


class GroupChatFile(models.Model):
    FILE_TYPES = [
        ('Attachment', 'Attachment'),
        ('Photo', 'Photo'),
        ('Video', 'Video'),
        ('Link', 'Link'),
        ('VoiceMessage', 'VoiceMessage'),
    ]

    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=50, choices=FILE_TYPES)
    file = models.FileField(upload_to='group_chat_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"File by {self.user.username} in {self.chat.group_name}"


class GroupChatLink(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Link for {self.chat.group_name}"
