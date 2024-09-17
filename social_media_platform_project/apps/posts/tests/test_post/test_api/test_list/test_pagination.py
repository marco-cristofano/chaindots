from rest_framework import status
from rest_framework.test import APITestCase

from apps.posts.services.post import PostService
from apps.users.services.social_media_user import SocialMediaUserService


class APIListPaginationTest(APITestCase):
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
            'content1'
        )
        self.post = PostService.create(
            self.user.username,
            'content2'
        )
        self.post = PostService.create(
            self.user_2.username,
            'content3'
        )

    def test_list_default_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        post = response.data[0]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content3')
        self.assertEqual(post['author'], self.user_2.id)
        self.assertIsNotNone(post['created_at'])
        post = response.data[1]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content2')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])
        post = response.data[2]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content1')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])

    def test_page_number_2_without_posts(self):
        params = {
            'page_number': 2
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_page_size_1(self):
        params = {
            'page_size': 1
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        post = response.data[0]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content3')
        self.assertEqual(post['author'], self.user_2.id)
        self.assertIsNotNone(post['created_at'])

    def test_page_size_2(self):
        params = {
            'page_size': 2
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        post = response.data[0]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content3')
        self.assertEqual(post['author'], self.user_2.id)
        self.assertIsNotNone(post['created_at'])
        post = response.data[1]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content2')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])

    def test_page_size_1_page_number_2(self):
        params = {
            'page_size': 1,
            'page_number': 2
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        post = response.data[0]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content2')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])
