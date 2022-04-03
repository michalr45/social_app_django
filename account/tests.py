from django.test import TestCase
from django.contrib.auth.models import User


class RegistrationTestCase(TestCase):

    def test_registration(self):
        data = {'username': 'test',
                'email': 'test@localhost.com',
                'password': 'testpassword123',
                'password2': 'testpassword123'}
        response = self.client.post('/account/register/', data)
        self.assertEqual(response.status_code, 200)


class AccountTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(self.credentials)

    def test_login(self):
        response = self.client.post('/account/login/', self.credentials)
        self.assertEqual(response.status_code, 200)
