from django.test import TestCase

from webapp.presenters.tweet_presenter import TweetPresenter
from webapp.tests.cleanup import clean_uploads
from webapp.tests.factories.user import UserFactory
from webapp.tests.factories.tweet import TweetFactory


class TweetPresenterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        tweet = TweetFactory(user=UserFactory(username='user'))
        cls.presenter = TweetPresenter(tweet)

    @classmethod
    def tearDownClass(cls):
        clean_uploads()

    def test_detects_image_is_present(self):
        self.assertTrue(self.presenter.has_image())

    def test_detects_image_is_not_present(self):
        noimage = TweetFactory(user=UserFactory(username='noimage'), image=None)
        self.assertFalse(TweetPresenter(noimage).has_image())

    def test_has_a_class_for_zero_likes(self):
        self.assertEqual(self.presenter.button_class(), 'tweet-footer__likes')

    def test_has_another_class_for_more_thanzero_likes(self):
        liked = TweetFactory(user=UserFactory(username='liked'), likes=1)
        self.assertEqual(TweetPresenter(liked).button_class(), 'tweet-footer__liked')
