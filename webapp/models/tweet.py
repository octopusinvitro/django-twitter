from django.conf import settings
from django.db import models


class Tweet(models.Model):
    TRUNCATED_MESSAGE_LENGTH = 40

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    message = models.TextField()
    image = models.ImageField(upload_to='attachments/', blank=True)
    likes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def fields(cls):
        return list(map(lambda field: field.attname, cls._meta.fields))[2:-3]

    def __str__(self):
        return f'{self.user.username}: {self.message[:self.TRUNCATED_MESSAGE_LENGTH]}...'
