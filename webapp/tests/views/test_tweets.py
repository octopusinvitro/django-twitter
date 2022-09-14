from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from webapp.models.tweet import Tweet
from webapp.tests.cleanup import clean_uploads
from webapp.tests.factories.tweet import TweetFactory
from webapp.tests.factories.user import UserFactory


class TweetsIndexTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        jane = UserFactory(username='Jane', password='password')
        TweetFactory(user=jane, message='hi')
        TweetFactory(user=jane, message='bye')

    @classmethod
    def tearDownClass(cls):
        clean_uploads()

    def login(self):
        credentials = {'username': 'Jane', 'password': 'password'}
        self.client.post(reverse('users_authentication'), credentials)

    def logout(self):
        self.client.get(reverse('users_logout'))

    def test_loads_url_successfully(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_has_url_available_by_name(self):
        response = self.client.get(reverse('tweets_index'))
        self.assertEqual(response.status_code, 200)

    def test_uses_index_template(self):
        response = self.client.get(reverse('tweets_index'))
        self.assertTemplateUsed(response, 'tweets/index.html')

    def test_displays_all_tweets(self):
        response = self.client.get(reverse('tweets_index'))
        self.assertContains(response, '<p>hi</p>', html=True)
        self.assertContains(response, '<p>bye</p>', html=True)

    def test_shows_login_and_join_if_not_logged(self):
        self.logout()
        response = self.client.get(reverse('tweets_index'))
        self.assertContains(response, reverse('users_login'))
        self.assertContains(response, reverse('users_new'))

    def test_does_not_show_login_and_join_if_logged(self):
        self.login()
        response = self.client.get(reverse('tweets_index'))
        self.assertNotContains(response, reverse('users_login'))
        self.assertNotContains(response, reverse('users_new'))

    def test_shows_new_tweet_logout_and_profile_if_logged(self):
        self.login()
        response = self.client.get(reverse('tweets_index'))
        self.assertContains(response, reverse('tweets_new'))
        self.assertContains(response, 'Profile</a>')
        self.assertContains(response, reverse('users_logout'))

    def test_does_not_show_new_tweet_logout_and_profile_if_not_logged(self):
        self.logout()
        response = self.client.get(reverse('tweets_index'))
        self.assertNotContains(response, reverse('tweets_new'))
        self.assertNotContains(response, 'Profile</a>')
        self.assertNotContains(response, reverse('users_logout'))


class TweetsNewTests(SimpleTestCase):
    def test_loads_url_successfully(self):
        response = self.client.get('/tweets/new')
        self.assertEqual(response.status_code, 200)

    def test_shows_new_tweet_form(self):
        response = self.client.get(reverse('tweets_new'))
        self.assertContains(response, 'action="/tweets"')

    def test_adds_CSRF_token(self):
        response = self.client.get(reverse('tweets_new'))
        self.assertIn('name="csrfmiddlewaretoken"', response.content.decode('utf-8'))


class TweetsCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.image_contents = open('webapp/tests/fixtures/test_image.png', 'rb').read()

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        clean_uploads()
        self.client.logout()

    def create_tweet(self, attributes={}):
        tweet = {
            'message': 'message',
            'image': SimpleUploadedFile('image.png', self.image_contents)
        }
        self.client.force_login(UserFactory())
        return self.client.post('/tweets', {**tweet, **attributes}, follow=True)

    def test_creates_valid_tweet(self):
        before = len(Tweet.objects.all())
        self.create_tweet()
        after = len(Tweet.objects.all())
        self.assertEqual(after, before + 1)

    def test_redirects_to_home_on_success(self):
        response = self.create_tweet()
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )

    def test_shows_success_message(self):
        response = self.create_tweet()
        self.assertIn('Success!', response.content.decode('utf-8'))

    def test_does_not_create_invalid_tweet(self):
        before = len(Tweet.objects.all())
        self.create_tweet({'message': ''})
        after = len(Tweet.objects.all())
        self.assertEqual(after, before)

    def test_redisplays_the_form_on_errors(self):
        response = self.create_tweet({'message': ''})
        self.assertContains(response, 'action="/tweets"')

    def test_shows_errors_on_page(self):
        response = self.create_tweet({'message': ''})
        self.assertContains(response, 'This field is required.')


class TweetsShowTests(TestCase):
    def setUp(self):
        # fixtures = f'{os.getcwd()}/webapp/tests/fixtures'
        # shutil.copyfile(f'/{fixtures}/test_image.png', f'{fixtures}/uploads/attachments/image.png')
        # image = SimpleUploadedFile('image.png', open(f'{fixtures}/test_image.png', 'rb').read())
        # self.valid_tweet = TweetFactory(user=UserFactory(), message='hello', image=image)
        self.valid_tweet = TweetFactory(user=UserFactory(), message='hello')

    def tearDown(self):
        clean_uploads()

    def test_loads_url_successfully(self):
        response = self.client.get(f'/tweets/{self.valid_tweet.id}')
        self.assertEqual(response.status_code, 200)

    def test_shows_tweet(self):
        response = self.client.get(reverse('tweets_show', kwargs={'id': self.valid_tweet.id}))
        self.assertContains(response, '<p>hello</p>')

    def test_shows_image_if_present(self):
        response = self.client.get(f'/tweets/{self.valid_tweet.id}')
        self.assertContains(response, f'<img src="{self.valid_tweet.image.url}')

    def test_does_not_show_image_if_not_present(self):
        tweet = TweetFactory(user=UserFactory(), image=None)
        response = self.client.get(f'/tweets/{tweet.id}')
        self.assertNotContains(response, '<a class="tweet-body__attachment"')

    # def test_loads_image_url_successfully(self):
    #     response = self.client.get(self.valid_tweet.image.url)
    #     self.assertEqual(response.status_code, 200)

    def test_throws_404_if_tweet_not_found(self):
        response = self.client.get(f'/tweets/{Tweet.objects.last().id + 1}')
        self.assertEqual(response.status_code, 404)


class TweetsLikesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.valid_tweet = TweetFactory(user=cls.user)

    @classmethod
    def tearDownClass(cls):
        clean_uploads()

    def setUp(self):
        self.client.force_login(self.user)

    def tearDown(self):
        self.client.logout()

    def update_likes(self, attributes={}):
        id = {'id': self.valid_tweet.id}
        return self.client.post('/tweets/likes', {**id, **attributes}, content_type='application/json')

    def test_increases_likes_by_one(self):
        before = self.valid_tweet.likes
        self.update_likes()
        self.valid_tweet.refresh_from_db()
        self.assertEqual(self.valid_tweet.likes, before + 1)

    def test_returns_likes_as_json(self):
        response = self.update_likes()
        self.valid_tweet.refresh_from_db()
        self.assertJSONEqual(response.content.decode('utf-8'), {'likes': self.valid_tweet.likes})
        self.assertEqual(response.status_code, 200)

    def test_errors_if_tweet_id_missing(self):
        response = self.client.post('/tweets/likes', '', content_type='application/json')
        self.assertJSONEqual(response.content.decode('utf-8'), {'error': 'Invalid data'})
        self.assertEqual(response.status_code, 400)

    def test_errors_if_tweet_id_empty(self):
        response = self.update_likes({'id': ''})
        self.assertJSONEqual(response.content.decode('utf-8'), {'error': 'Invalid data'})
        self.assertEqual(response.status_code, 400)

    def test_errors_if_missing_tweet(self):
        response = self.update_likes({'id': self.valid_tweet.id + 1})
        self.assertJSONEqual(response.content.decode('utf-8'), {'error': 'Tweet not found'})
        self.assertEqual(response.status_code, 404)
