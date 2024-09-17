from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.services.social_media_user import SocialMediaUserService
from apps.posts.models.post import Post


class APICreatePostTest(APITestCase):
    url = '/api/posts/'

    def setUp(self):
        self.user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )

    def test_create(self):
        params = {
            'author': self.user.id,
            'content': 'content',
        }
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        post = response.data
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])
        post = Post.objects.get(id=post['id'])
        self.assertEqual(post.content, 'content')
        self.assertEqual(post.author.id, self.user.id)
        self.assertIsNotNone(post.created_at)


class APICreatePostFailTest(APITestCase):
    url = '/api/posts/'

    def setUp(self):
        self.user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )

    def test_without_author(self):
        params = {
            'content': 'content',
        }
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'author', status_code=400)
        self.assertContains(response, 'required', status_code=400)

    def test_without_content(self):
        params = {
            'author': self.user.id,
        }
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'content', status_code=400)
        self.assertContains(response, 'required', status_code=400)

    def test_blank_content(self):
        params = {
            'author': self.user.id,
            'content': ''
        }
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'content', status_code=400)
        self.assertContains(response, 'blank', status_code=400)
