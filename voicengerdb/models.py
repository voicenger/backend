from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pictures = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    notifications_enabled = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(blank=True, null=True)
    is_online = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Chat(models.Model):
    PRIVATE = 'Private'
    GROUP = 'Group'
    ANONIM_GROUP = 'Anonim Group'
    CHANNEL = 'Channel'

    CHAT_TYPE_CHOICES = [
        (PRIVATE, 'Private'),
        (GROUP, 'Group'),
        (ANONIM_GROUP, 'Anonim Group'),
        (CHANNEL, 'Channel'),
    ]

    chat_type = models.CharField(max_length=20, choices=CHAT_TYPE_CHOICES)
    chat_image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    closed_at = models.DateTimeField(blank=True, null=True)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='last_message_in_chat')

    def __str__(self):
        return f"{self.chat_type} Chat"


class ChatParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user.username} in {self.chat.id}"


class Message(models.Model):
    TEXT = 'text'
    AUDIO = 'audio'
    VIDEO = 'video'
    IMAGE = 'image'
    FILE = 'file'

    MESSAGE_TYPE_CHOICES = [
        (TEXT, 'Text'),
        (AUDIO, 'Audio'),
        (VIDEO, 'Video'),
        (IMAGE, 'Image'),
        (FILE, 'File'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    video_file = models.FileField(upload_to='video/', blank=True, null=True)
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)
    attached_file = models.FileField(upload_to='files/', blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default=TEXT)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.user.username} in {self.chat.id}"


class MessageReadReceipt(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    chat_participant = models.ForeignKey(ChatParticipant, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat_participant.user.username} read message {self.message.id}"
