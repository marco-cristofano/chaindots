from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.services.social_media_user import SocialMediaUserService

from apps.posts.services.post import PostService


class APIPostCommentsTest(APITestCase):
    url = '/api/posts/'

    def setUp(self):
        self.user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        self.user_2 = SocialMediaUserService.create(
            username='username2',
            email='email2@email.com',
            password='password'
        )
        self.post = PostService.create(
            self.user.username,
            'content'
        )

    def get_url(self, post_id):
        return "{}{}/comments/".format(self.url, post_id)

    def test_create(self):
        params = {
            'author': self.user_2.id,
            'comment': 'comment1',
            'post': self.post.id
        }
        url = self.get_url(self.post.id)
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = response.data
        self.assertEqual(len(comment), 4)
        self.assertIsNotNone(comment['id'])
        self.assertEqual(comment['comment'], 'comment1')
        self.assertEqual(comment['author']['id'], self.user_2.id)
        self.assertEqual(comment['author']['email'], self.user_2.email)
        self.assertEqual(comment['author']['username'], self.user_2.username)
        self.assertIsNotNone(comment['created_at'])


class APIPostCommentsFailTest(APITestCase):
    url = '/api/posts/'

    def setUp(self):
        self.user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        self.user_2 = SocialMediaUserService.create(
            username='username2',
            email='email2@email.com',
            password='password'
        )
        self.post = PostService.create(
            self.user.username,
            'content'
        )

    def get_url(self, post_id):
        return "{}{}/comments/".format(self.url, post_id)

    def test_without_author(self):
        params = {
            'comment': 'comment1',
            'post': self.post.id
        }
        url = self.get_url(self.post.id)
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(
            response, 'author', status_code=status.HTTP_400_BAD_REQUEST
        )
        self.assertContains(
            response, 'required', status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_without_comment(self):
        params = {
            'author': self.user_2.id,
            'post': self.post.id
        }
        url = self.get_url(self.post.id)
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response, 'comment', status_code=status.HTTP_400_BAD_REQUEST
        )
        self.assertContains(
            response, 'required', status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_blank_comment(self):
        params = {
            'author': self.user_2.id,
            'comment': '',
            'post': self.post.id
        }
        url = self.get_url(self.post.id)
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response, 'comment', status_code=status.HTTP_400_BAD_REQUEST
        )
        self.assertContains(
            response, 'blank', status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_without_post(self):
        params = {
            'author': self.user_2.id,
            'comment': 'comment1',
        }
        url = self.get_url(self.post.id)
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response, 'post', status_code=status.HTTP_400_BAD_REQUEST
            )
        self.assertContains(
            response, 'required', status_code=status.HTTP_400_BAD_REQUEST
        )
