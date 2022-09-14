from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    MAXIMUM_LENGTH = 128
    DEFAULT_AVATAR = 'default_avatar.png'

    username = models.CharField(max_length=MAXIMUM_LENGTH, unique=True)
    email = models.CharField(max_length=MAXIMUM_LENGTH, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    display_name = models.CharField(max_length=MAXIMUM_LENGTH)
    avatar = models.ImageField(upload_to='avatars/', default=DEFAULT_AVATAR, help_text=_('avatar_help_text'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password', 'display_name']

    @classmethod
    def fields(cls):
        return ['email', 'username', 'display_name', 'avatar']

    @classmethod
    def update_fields(cls):
        return ['email', 'display_name', 'avatar']

    def __str__(self):
        return self.username
