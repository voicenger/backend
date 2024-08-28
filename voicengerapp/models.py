from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Field for save identificator user from Auth0
    auth0_sub = models.CharField(max_length=255, unique=True)

    objects = UserManager()  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Chat(models.Model):
    """
    Class: Chat

    A class representing a chat session in the application.

    Attributes:
    - name (CharField): A field representing the name of the chat.
    - participants (ManyToManyField): A field representing the participants in the chat session.
    - created_at (DateTimeField): A field representing the date and time when the chat session was created.
    - updated_at (DateTimeField): A field representing the date and time when the chat session was last updated.

    Methods:
    - __str__(): Returns a string representation of the chat session.
    - save(self, *args, **kwargs): Automatically sets the chat name if it's not provided.

    """
    name = models.CharField(max_length=255, blank=True, null=True, default='NewChat')
    participants = models.ManyToManyField(User, through='UserChat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Chat {self.id}"



class Message(models.Model):
    """
    Class representing a message in a chat.

    Attributes:
        chat (ForeignKey): The chat to which the message belongs.
        sender (ForeignKey): The user who sent the message.
        text (TextField): The content of the message.
        timestamp (DateTimeField): The timestamp when the message was created.
        is_read (BooleanField): A flag indicating if the message has been read.

    Methods:
        __str__(self): Returns a string representation of the message.

    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} in chat {self.chat.id}"


class UserChat(models.Model):
    """

    This class represents a relationship between a User and a Chat in a messaging app.

    Attributes:
    - user: A foreign key to the User model, representing the user involved in the chat.
    - chat: A foreign key to the Chat model, representing the chat the user is participating in.
    - last_read_message: A foreign key to the Message model, representing the last message that the user has read in the chat. It can be null or blank.

    Methods:
    - __str__(): Returns a string representation of the UserChat object.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    last_read_message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    def clean(self):
        super().clean()
        if UserChat.objects.filter(chat=self.chat).count() >= 2:
            raise ValidationError("This chat already has two participants.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"