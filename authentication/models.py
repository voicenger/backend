from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """
    Custom User model with additional fields for tracking registration method
    and other user-specific details.
    """
    email = models.EmailField(max_length=254, unique=True)
    REGISTRATION_CHOICES = [
        ('email', _('Email')),
        ('google', _('Google')),
    ]
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )

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
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined']
        verbose_name = _('user')
        verbose_name_plural = _('users')


# Define the Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    nickname = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=150, null=True, blank=True)

    # String representation of the Profile model
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
