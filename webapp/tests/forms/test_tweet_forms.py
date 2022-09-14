from django.test import TestCase

from webapp.forms.tweet_forms import CreateTweetForm
from webapp.tests.cleanup import clean_uploads


class CreateTweetFormTests(TestCase):
    def tearDown(self):
        clean_uploads()

    def test_accepts_valid_tweet_form_data(self):
        valid_data = {'message': 'message'}
        self.assertTrue(CreateTweetForm(data=valid_data).is_valid())

    def test_rejects_invalid_tweet_form_data(self):
        valid_data = {'message': ''}
        self.assertFalse(CreateTweetForm(data=valid_data).is_valid())
