from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


class UserActionsTestCase(TestCase):

    def setUp(self):
        username = 'test'
        password = 'testpassword123'
        self.user = User.objects.create_user(username=username)
        self.user.set_password(password)
        self.user.save()
        self.client.login(username=username, password=password)

    def test_create_post(self):
        content = 'something'
        post = self.client.post('/dashboard/', data={'user': self.user,
                                                          'text': content})
        self.assertEqual(post.status_code, 302)

    def test_post_like(self):
        post = Post.objects.create(user=self.user, text='Lorem ipsum')
        like = self.client.post('/like/', data={'id': post.id,
                                                'action': 'like'})
        self.assertEqual(like.status_code, 200)

    def test_post_detail(self):
        post = Post.objects.create(user=self.user, text='Lorem ipsum')
        response = self.client.get(f'/post/{post.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        post = Post.objects.create(user=self.user, text='Lorem ipsum')
        delete = self.client.post(f'/post/delete/{post.id}/')
        self.assertEqual(delete.status_code, 302)

    def test_create_comment(self):
        post = Post.objects.create(user=self.user, text='Lorem ipsum')
        content = 'comment'
        comment = self.client.post(f'/post/{post.slug}/', data={'author': self.user,
                                                                'post': post,
                                                                'text': content})
        self.assertEqual(comment.status_code, 302)

    def test_comment_delete(self):
        post = Post.objects.create(user=self.user, text='Lorem ipsum')
        comment = Comment.objects.create(author=self.user, text='Lorem ipsum', post=post)
        delete = self.client.post(f'/comment/delete/{comment.id}/')
        self.assertEqual(delete.status_code, 302)
