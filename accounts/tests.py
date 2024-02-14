from datetime import datetime, date
from unittest import TestCase

from django.contrib.auth.models import User

from accounts.models import Profile


# Create your tests here.

class UserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user('test_user', 'test@example.com', 'testpassword')
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser('superuser', 'superuser@example.com', 'superpassword')
        self.assertEqual(user.username, 'superuser')
        self.assertEqual(user.email, 'superuser@example.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class ProfileTest(TestCase):

    def setUp(self):
        birth_date = date(1980, 10, 4)
        user = User.objects.create(username='test_user123', email='test@example.com', password='testpassword')
        self.profile = Profile.objects.create(user=user,
                                               phone_number='+420 777 777 777',
                                               birth_date=birth_date,
                                               street='My Street',
                                               house_number=123,
                                               city='My City',
                                               country='My Country',
                                               postal_code='12345')

    def test_profile_created(self):
        self.assertEqual(self.profile.user.username, 'test_user123')
        self.assertEqual(self.profile.phone_number, '+420 777 777 777')
        self.assertEqual(self.profile.birth_date, date(1980, 10, 4))
        self.assertEqual(self.profile.street, 'My Street')
        self.assertEqual(self.profile.house_number, 123)
        self.assertEqual(self.profile.city, 'My City')
        self.assertEqual(self.profile.country, 'My Country')
        self.assertEqual(self.profile.postal_code, '12345')