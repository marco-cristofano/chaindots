from rest_framework import status
from utils.tests.apt_test import CustomAPITestCase as APITestCase
from apps.users.services.social_media_user import SocialMediaUserService

from apps.posts.services.post import PostService
from apps.posts.services.comment import CommentService


class APIGetCommentsTest(APITestCase):
    url = '/api/posts/'

    def setUp(self):
        super().setUp()
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

    def test_without_comments(self):
        url = self.get_url(self.post.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_one_comment(self):
        CommentService.create(self.user_2.username, self.post, 'comment1')

        url = self.get_url(self.post.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        comment = response.data[0]
        self.assertIsNotNone(comment['id'])
        self.assertEqual(comment['comment'], 'comment1')
        self.assertEqual(comment['author']['id'], self.user_2.id)
        self.assertEqual(comment['author']['email'], self.user_2.email)
        self.assertEqual(comment['author']['username'], self.user_2.username)
        self.assertIsNotNone(comment['created_at'])

    def test_retrieve_three_comments(self):
        CommentService.create(self.user_2.username, self.post, 'comment1')
        CommentService.create(self.user_2.username, self.post, 'comment2')
        CommentService.create(self.user_2.username, self.post, 'comment3')

        url = self.get_url(self.post.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        comment = response.data[0]
        self.assertIsNotNone(comment['id'])
        self.assertEqual(comment['comment'], 'comment3')
        self.assertEqual(comment['author']['id'], self.user_2.id)
        self.assertEqual(comment['author']['email'], self.user_2.email)
        self.assertEqual(comment['author']['username'], self.user_2.username)
        self.assertIsNotNone(comment['created_at'])
        comment = response.data[1]
        self.assertIsNotNone(comment['id'])
        self.assertEqual(comment['comment'], 'comment2')
        self.assertEqual(comment['author']['id'], self.user_2.id)
        self.assertEqual(comment['author']['email'], self.user_2.email)
        self.assertEqual(comment['author']['username'], self.user_2.username)
        self.assertIsNotNone(comment['created_at'])
        comment = response.data[2]
        self.assertIsNotNone(comment['id'])
        self.assertEqual(comment['comment'], 'comment1')
        self.assertEqual(comment['author']['id'], self.user_2.id)
        self.assertEqual(comment['author']['email'], self.user_2.email)
        self.assertEqual(comment['author']['username'], self.user_2.username)
        self.assertIsNotNone(comment['created_at'])
