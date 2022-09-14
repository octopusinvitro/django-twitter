import os
from django.conf import settings


def clean_uploads():
    avatars = os.path.join(settings.MEDIA_ROOT, 'avatars')
    for image in os.listdir(avatars):
        os.remove(os.path.join(avatars, image))

    attachments = os.path.join(settings.MEDIA_ROOT, 'attachments')
    for image in os.listdir(attachments):
        os.remove(os.path.join(attachments, image))
