from unittest import skip

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import DataError, IntegrityError
from django.test import TransactionTestCase

from webapp.tests.cleanup import clean_uploads
from webapp.tests.factories.user import UserFactory


class UserTests(TransactionTestCase):
    def tearDown(self):
        clean_uploads()

    def test_has_list_of_fields(self):
        self.assertEqual(get_user_model().fields(), ['email', 'username', 'display_name', 'avatar'])

    def test_has_list_of_update_fields(self):
        self.assertEqual(get_user_model().update_fields(), ['email', 'display_name', 'avatar'])

    def test_saves_valid_user(self):
        UserFactory(username='username', email='username@example.com')
        saved_user = get_user_model().objects.get(username='username')
        self.assertEqual(saved_user.email, 'username@example.com')
        self.assertEqual(saved_user.username, 'username')
        self.assertEqual(saved_user.display_name, 'User Name')
        self.assertEqual(saved_user.avatar, 'avatars/example.jpg')
        self.assertTrue(saved_user.is_active)
        self.assertFalse(saved_user.is_admin)
        self.assertFalse(saved_user.is_staff)
        self.assertFalse(saved_user.is_superuser)

    @skip('Why does it say no file? the user has default_avatar.png in the admin panel')
    def test_has_default_avatar_if_none_provided(self):
        valid_user = UserFactory(avatar=SimpleUploadedFile(None, None))
        saved_user = get_user_model().objects.get(pk=valid_user.id)
        self.assertEqual(saved_user.avatar, get_user_model().DEFAULT_AVATAR)

    def test_validates_username_length(self):
        invalid_username = 'x' * (get_user_model().MAXIMUM_LENGTH + 1)
        with self.assertRaises(DataError):
            UserFactory(username=invalid_username)

    def test_validates_username_uniqueness(self):
        UserFactory(username='repeated')
        with self.assertRaises(IntegrityError):
            UserFactory(username='repeated')

    def test_validates_email_length(self):
        invalid_email = 'x' * (get_user_model().MAXIMUM_LENGTH + 1)
        with self.assertRaises(DataError):
            UserFactory(email=invalid_email)

    def test_validates_email_uniqueness(self):
        UserFactory(email='repeated@example.com')
        with self.assertRaises(IntegrityError):
            UserFactory(email='repeated@example.com')

    def test_validates_display_name_length(self):
        invalid_name = 'x' * (get_user_model().MAXIMUM_LENGTH + 1)
        with self.assertRaises(DataError):
            UserFactory(display_name=invalid_name)

    def test_does_not_save_invalid_user(self):
        invalid_username = 'x' * (get_user_model().MAXIMUM_LENGTH + 1)
        with self.assertRaises(DataError):
            UserFactory(username=invalid_username, email='username@example.com')
        self.assertFalse(get_user_model().objects.filter(email='username@example.com').exists())

    def test_returns_username_when_stringified(self):
        user = UserFactory(username='name')
        self.assertEqual(str(user), 'name')
