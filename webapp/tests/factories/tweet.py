import factory

from django.utils import timezone


class TweetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'webapp.Tweet'

    user = factory.SubFactory('.user.UserFactory')
    message = 'message'
    image = factory.django.ImageField()
    created_at = timezone.now()
    updated_at = timezone.now()
