from django.db.utils import DataError
from django.test import TransactionTestCase
from django.utils import timezone

from webapp.models.tweet import Tweet
from webapp.tests.cleanup import clean_uploads
from webapp.tests.factories.tweet import TweetFactory
from webapp.tests.factories.user import UserFactory


class TweetTests(TransactionTestCase):
    def tearDown(self):
        clean_uploads()

    def test_has_updated_list_of_fields(self):
        self.assertEqual(Tweet.fields(), ['message', 'image'])

    def test_saves_valid_tweet(self):
        valid_tweet = TweetFactory(user=UserFactory(username='username'))
        saved_tweet = Tweet.objects.get(pk=valid_tweet.id)
        self.assertEqual(saved_tweet.user.username, 'username')
        self.assertEqual(saved_tweet.message, 'message')
        self.assertEqual(saved_tweet.image, 'attachments/example.jpg')

    def test_considers_image_optional(self):
        valid_tweet = TweetFactory(user=UserFactory(), image=None)
        saved_tweet = Tweet.objects.get(pk=valid_tweet.id)
        self.assertEqual(saved_tweet.image.name, '')

    def test_does_not_save_invalid_tweet(self):
        date = timezone.now()
        with self.assertRaises(DataError):
            TweetFactory(user=UserFactory(), created_at=None, updated_at=date)
        self.assertFalse(Tweet.objects.filter(updated_at=date).exists())

    def test_truncates_message_and_adds_ellipsis_when_stringified(self):
        message = 'Nap all day cat dog hate mouse eat string barf pillow no baths hate everything.'
        tweet = TweetFactory(user=UserFactory(username='name'), message=message)
        self.assertEqual(str(tweet), 'name: Nap all day cat dog hate mouse eat strin...')
