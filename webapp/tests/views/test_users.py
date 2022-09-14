from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.models import model_to_dict
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from webapp.tests.cleanup import clean_uploads
from webapp.tests.factories.tweet import TweetFactory
from webapp.tests.factories.user import UserFactory


class UsersNewTests(SimpleTestCase):
    def test_loads_url_successfully(self):
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)

    def test_shows_new_tweet_form(self):
        response = self.client.get(reverse('users_new'))
        self.assertContains(response, 'action="/users"')

    def test_adds_CSRF_token(self):
        response = self.client.get(reverse('users_new'))
        self.assertIn('name="csrfmiddlewaretoken"', response.content.decode('utf-8'))


class UsersCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.image_contents = open('webapp/tests/fixtures/test_image.png', 'rb').read()

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        clean_uploads()

    def create_user(self, attributes={}):
        password = 'a_very_uncommon_password'
        user = {
            'username': 'username', 'password1': password, 'password2': password,
            'email': 'username@example.com', 'display_name': 'Username',
            'avatar': SimpleUploadedFile('avatar.png', self.image_contents)
        }
        return self.client.post('/users', {**user, **attributes}, follow=True)

    def test_creates_valid_user(self):
        before = len(get_user_model().objects.all())
        self.create_user()
        after = len(get_user_model().objects.all())
        self.assertEqual(after, before + 1)

    def test_redirects_to_login_on_success(self):
        response = self.create_user()
        self.assertRedirects(
            response, reverse('users_login'), status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_shows_success_message(self):
        response = self.create_user()
        self.assertIn(_('join_success_message'), response.content.decode('utf-8'))

    def test_does_not_create_invalid_user(self):
        before = len(get_user_model().objects.all())
        self.create_user({'password2': 'different'})
        after = len(get_user_model().objects.all())
        self.assertEqual(after, before)

    def test_redisplays_form_on_errors(self):
        response = self.create_user({'username': ''})
        self.assertContains(response, 'action="/users"')

    def test_shows_errors_on_page(self):
        response = self.create_user({'display_name': ''})
        self.assertContains(response, 'This field is required.')


class UsersShowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_user = UserFactory(username='janedoe')

    @classmethod
    def tearDownClass(cls):
        clean_uploads()

    def test_loads_url_successfully(self):
        response = self.client.get('/users/janedoe')
        self.assertEqual(response.status_code, 200)

    def test_shows_user(self):
        response = self.client.get(reverse('users_show', kwargs={'username': 'janedoe'}))
        self.assertContains(response, '@janedoe</p>')

    def test_shows_edit_link_if_logged(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('users_show', kwargs={'username': 'janedoe'}))
        self.assertContains(response, reverse('users_edit'))

    # def test_does_not_show_edit_link_if_not_logged(self):
    #     UserFactory(username='not_logged')
    #     response = self.client.get(reverse('users_show', kwargs={'username': 'not_logged'}))
    #     self.assertNotContains(response, reverse('users_edit'))

    def test_shows_user_tweets_if_present(self):
        TweetFactory(user=self.valid_user, message='Hello!')
        response = self.client.get(reverse('users_show', kwargs={'username': 'janedoe'}))
        self.assertContains(response, '<p>Hello!</p>')

    def test_shows_no_user_tweets_if_not_present(self):
        response = self.client.get(reverse('users_show', kwargs={'username': 'janedoe'}))
        self.assertNotContains(response, 'tweet-list__item')

    def test_throws_404_if_user_not_found(self):
        response = self.client.get('/users/inexistent')
        self.assertEqual(response.status_code, 404)


class UsersEditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_user = UserFactory(username='rosalind', email='rosalind@franklin.com')

    @classmethod
    def tearDownClass(cls):
        clean_uploads()

    def setUp(self):
        self.client.force_login(self.valid_user)

    def tearDown(self):
        self.client.logout()

    def test_loads_url_successfully(self):
        response = self.client.get('/users/edit')
        self.assertEqual(response.status_code, 200)

    def test_shows_edit_tweets_form(self):
        response = self.client.get(reverse('users_edit'))
        self.assertContains(response, f'action="/users/{self.valid_user.id}"')

    def test_fills_in_form_with_user_data(self):
        response = self.client.get(reverse('users_edit'))
        self.assertContains(response, 'value="rosalind@franklin.com"')

    def test_displays_username_but_not_editable(self):
        response = self.client.get(reverse('users_edit'))
        self.assertContains(response, '@rosalind</h2>')


class UsersUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_user = UserFactory(username='lisemeitner', email='lisemeitner@example.com')

    @classmethod
    def tearDownClass(cls):
        clean_uploads()

    def setUp(self):
        self.client.force_login(self.valid_user)

    def tearDown(self):
        self.client.logout()

    def update_user(self, attributes={}):
        payload = {**model_to_dict(self.valid_user), **attributes}
        id = payload['id']
        return self.client.post(f'/users/{id}', payload, follow=True)

    def test_updates_valid_user(self):
        self.update_user({'email': 'different@example.com'})
        self.assertEqual(get_user_model().objects.get(username='lisemeitner').email, 'different@example.com')

    def test_redirects_to_profile_on_success(self):
        response = self.update_user({'email': 'different@example.com'})
        self.assertRedirects(
            response, reverse('users_show', kwargs={'username': 'lisemeitner'}),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_displays_success_message(self):
        response = self.update_user({'email': 'different@example.com'})
        self.assertContains(response, 'updated')

    def test_does_not_update_user_if_ids_dont_match(self):
        id = self.valid_user.id
        self.update_user({'id': id + 1})
        self.assertEqual(get_user_model().objects.get(username='lisemeitner').id, id)

    def test_displays_error_if_ids_dont_match(self):
        response = self.update_user({'id': self.valid_user.id + 1})
        self.assertContains(response, 'can not update')

    def test_redirects_to_edit_if_ids_dont_match(self):
        response = self.update_user({'id': self.valid_user.id + 1})
        self.assertRedirects(
            response, reverse('users_edit'), status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_does_not_update_invalid_user(self):
        self.update_user({'email': ''})
        self.assertEqual(get_user_model().objects.get(username='lisemeitner').email, 'lisemeitner@example.com')

    def test_redisplays_form_if_invalid_user(self):
        response = self.update_user({'email': ''})
        action = reverse('users_update', kwargs={'id': self.valid_user.id})
        self.assertContains(response, f'action="{action}"')


class UsersLoginTests(SimpleTestCase):
    def test_loads_url_successfully(self):
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)

    def test_shows_user_login_form(self):
        response = self.client.get(reverse('users_login'))
        self.assertContains(response, 'action="/users/authentication"')

    def test_adds_CSRF_token(self):
        response = self.client.get(reverse('users_login'))
        self.assertIn('name="csrfmiddlewaretoken"', response.content.decode('utf-8'))


class UsersAuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(username='emynoether', password='Very123Secure')
        UserFactory(username='inactive', password='Very456Inactive', is_active=False)

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        clean_uploads()

    def authenticate(self, overwrites={}):
        credentials = {'username': 'emynoether', 'password': 'Very123Secure'}
        return self.client.post('/users/authentication', {**credentials, **overwrites})

    def test_logs_user_on_success(self):
        response = self.authenticate()
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_redirects_to_home_on_success(self):
        response = self.authenticate()
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )

    def test_does_not_log_inactive_user(self):
        credentials = {'username': 'inactive', 'password': 'Very456Inactive'}
        response = self.authenticate(credentials)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_shows_inactive_user_error(self):
        credentials = {'username': 'inactive', 'password': 'Very456Inactive'}
        response = self.authenticate(credentials)
        self.assertContains(response, 'Please enter a correct username')

    def test_does_not_log_missing_user(self):
        credentials = {'username': 'inexistent', 'password': 'irrelevant'}
        response = self.authenticate(credentials)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_shows_missing_user_error(self):
        credentials = {'username': 'inexistent', 'password': 'irrelevant'}
        response = self.authenticate(credentials)
        self.assertContains(response, 'Please enter a correct username')

    def test_does_not_work_with_invalid_data(self):
        response = self.authenticate({'username': '', 'password': ''})
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_shows_invalid_data_error(self):
        response = self.authenticate({'username': '', 'password': ''})
        self.assertContains(response, 'This field is required.')


class UsersLogoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(username='meghamilton', password='Very123Secure')

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        clean_uploads()

    def test_logs_user_out_on_success(self):
        self.client.login(username='meghamilton', password='Very123Secure')
        logged = self.client.logout()
        self.assertFalse(logged)

    def test_redirects_to_home_on_success(self):
        self.client.login(username='meghamilton', password='Very123Secure')
        response = self.client.get('/users/logout')
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
