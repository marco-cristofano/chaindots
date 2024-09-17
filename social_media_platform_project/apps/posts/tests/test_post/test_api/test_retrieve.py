from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.services.social_media_user import SocialMediaUserService

from apps.posts.services.post import PostService
from apps.posts.services.comment import CommentService


class APIRetrieveTest(APITestCase):
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
        return "{}{}/".format(self.url, post_id)

    def test_retrieve(self):
        url = self.get_url(self.post.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        post = response.data
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])
        comments = post['last_comments']
        self.assertEqual(len(comments), 0)

    def test_retrieve_one_comments(self):
        CommentService.create(self.user_2.username, self.post, 'comment1')

        url = self.get_url(self.post.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        post = response.data
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])
        comments = post['last_comments']
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]['author']['id'], self.user_2.id)
        self.assertEqual(
            comments[0]['author']['username'], self.user_2.username
        )
        self.assertEqual(
            comments[0]['author']['email'], self.user_2.email
        )
        self.assertEqual(comments[0]['comment'], 'comment1')
        self.assertIsNotNone(comments[0]['created_at'])

    def test_retrieve_three_comments(self):
        CommentService.create(self.user_2.username, self.post, 'comment1')
        CommentService.create(self.user_2.username, self.post, 'comment2')
        CommentService.create(self.user_2.username, self.post, 'comment3')

        url = self.get_url(self.post.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        post = response.data
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])
        comments = post['last_comments']
        self.assertEqual(len(comments), 3)
        self.assertEqual(comments[0]['author']['id'], self.user_2.id)
        self.assertEqual(
            comments[0]['author']['username'], self.user_2.username
        )
        self.assertEqual(
            comments[0]['author']['email'], self.user_2.email
        )
        self.assertEqual(comments[0]['comment'], 'comment3')
        self.assertIsNotNone(comments[0]['created_at'])
        self.assertEqual(comments[1]['author']['id'], self.user_2.id)
        self.assertEqual(
            comments[1]['author']['username'], self.user_2.username
        )
        self.assertEqual(
            comments[1]['author']['email'], self.user_2.email
        )
        self.assertEqual(comments[1]['comment'], 'comment2')
        self.assertIsNotNone(comments[1]['created_at'])
        self.assertEqual(comments[2]['author']['id'], self.user_2.id)
        self.assertEqual(
            comments[2]['author']['username'], self.user_2.username
        )
        self.assertEqual(
            comments[2]['author']['email'], self.user_2.email
        )
        self.assertEqual(comments[2]['comment'], 'comment1')
        self.assertIsNotNone(comments[2]['created_at'])
