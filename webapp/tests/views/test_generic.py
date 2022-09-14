from unittest.mock import patch

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.test import SimpleTestCase, TestCase


class Tweets400Tests(SimpleTestCase):
    @patch('webapp.models.tweet.Tweet.objects.all', side_effect=SuspiciousOperation)
    def test_shows_custom_400_page(self, mock):
        response = self.client.get('/')
        self.assertIn('client error', response.content.decode('utf-8'))

    @patch('webapp.models.tweet.Tweet.objects.all', side_effect=SuspiciousOperation)
    def test_has_400_status_code(self, mock):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 400)


class Tweets403Tests(TestCase):
    @patch('webapp.models.tweet.Tweet.objects.all', side_effect=PermissionDenied)
    def test_shows_custom_403_page(self, mock):
        response = self.client.get('/')
        self.assertIn('permissions', response.content.decode('utf-8'))

    @patch('webapp.models.tweet.Tweet.objects.all', side_effect=PermissionDenied)
    def test_has_403_status_code(self, mock):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 403)


class Tweets404Tests(SimpleTestCase):
    def test_shows_custom_404_page(self):
        response = self.client.get('/inexistent')
        self.assertIn('Oooops', response.content.decode('utf-8'))

    def test_has_404_status_code(self):
        response = self.client.get('/inexistent')
        self.assertEqual(response.status_code, 404)


# class Tweets500Tests(SimpleTestCase):
#     @patch('webapp.models.tweet.Tweet.objects.all', side_effect=ResponseServerError)
#     def test_shows_custom_500_page(self, mock):
#         response = self.client.get('/')
#         self.assertIn('on our side', response.content.decode('utf-8'))
    #
    # @patch('webapp.models.tweet.Tweet.objects.all', side_effect=ResponseServerError)
    # def test_has_500_status_code(self, mock):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 500)
