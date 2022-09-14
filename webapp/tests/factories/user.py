import factory

from django.conf import settings
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda number: 'username%s' % number)
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email = factory.LazyAttribute(lambda username: '%s@example.org' % username.username)
    display_name = 'User Name'
    avatar = factory.django.ImageField()
    is_active = True
    created_at = timezone.now()
    updated_at = timezone.now()
