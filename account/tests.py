from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Follow


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

    def test_logout(self):
        response = self.client.post('/account/logout/')
        self.assertEqual(response.status_code, 200)


class ViewsTestCase(TestCase):

    def setUp(self):
        username = 'test'
        password = 'testpassword123'
        self.user = User.objects.create_user(username=username)
        self.user.set_password(password)
        self.user.save()
        Profile.objects.create(user=self.user)
        login = self.client.login(username=username, password=password)
        self.assertTrue(login)

    def test_follow(self):
        user_to_follow = User.objects.create_user(username='test2')
        user_to_follow.set_password('testpassword123')
        user_to_follow.save()
        follow = Follow.objects.get_or_create(user_from=self.user, user_to=user_to_follow)
        self.assertTrue(follow)

    def test_get_user_detail(self):
        response = self.client.get('/account/users/test/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_profile(self):
        response = self.client.get('/account/edit/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_posts(self):
        response = self.client.get('/user/posts/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_comments(self):
        response = self.client.get('/user/comments/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_likes(self):
        response = self.client.get('/user/likes/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_follows(self):
        response = self.client.get('/user/follows/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_bookshelf(self):
        response = self.client.get('/books/user/bookshelf/')
        self.assertEqual(response.status_code, 200)

