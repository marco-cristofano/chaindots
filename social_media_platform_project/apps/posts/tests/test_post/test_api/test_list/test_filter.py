from datetime import timedelta

from rest_framework import status
from utils.tests.apt_test import CustomAPITestCase as APITestCase

from apps.posts.services.post import PostService
from apps.users.services.social_media_user import SocialMediaUserService


class APIListFilterTest(APITestCase):
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
        self.post_1 = PostService.create(
            self.user.username,
            'content1'
        )
        self.post_2 = PostService.create(
            self.user.username,
            'content2'
        )
        self.post_3 = PostService.create(
            self.user_2.username,
            'content3'
        )

    @staticmethod
    def datetime_to_str(datetime):
        return datetime.strftime("%Y-%m-%d")

    def test_list_filter_author_one_post(self):
        params = {
            'author_id': self.user_2.id
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        post = response.data[0]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content3')
        self.assertEqual(post['author'], self.user_2.id)
        self.assertIsNotNone(post['created_at'])

    def test_list_filter_author_two_post(self):
        params = {
            'author_id': self.user.id
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        post = response.data[0]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content2')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])
        post = response.data[1]
        self.assertIsNotNone(post['id'])
        self.assertEqual(post['content'], 'content1')
        self.assertEqual(post['author'], self.user.id)
        self.assertIsNotNone(post['created_at'])

    def test_list_filter_author_zero_posts(self):
        params = {
            'author_id': 100
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_from_date_same_date(self):
        from_date = self.datetime_to_str(self.post_3.created_at)
        params = {
            'from_date': from_date
        }
        response = self.client.get(self.url, params)
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

    def test_list_filter_from_date_minor_date(self):
        from_date = self.datetime_to_str(
            self.post_3.created_at - timedelta(days=1)
        )
        params = {
            'from_date': from_date
        }
        response = self.client.get(self.url, params)
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

    def test_list_filter_from_date_major_date(self):
        from_date = self.datetime_to_str(
            self.post_3.created_at + timedelta(days=1)
        )
        params = {
            'from_date': from_date
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_to_date_same_date(self):
        from_date = self.datetime_to_str(self.post_3.created_at)
        params = {
            'to_date': from_date
        }
        response = self.client.get(self.url, params)
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

    def test_list_filter_to_date_major_date(self):
        from_date = self.datetime_to_str(
            self.post_3.created_at + timedelta(days=1)
        )
        params = {
            'to_date': from_date
        }
        response = self.client.get(self.url, params)
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

    def test_list_filter_to_date_minor_date(self):
        from_date = self.datetime_to_str(
            self.post_3.created_at - timedelta(days=1)
        )
        params = {
            'to_date': from_date
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_from_date_to_date_same_date(self):
        date = self.datetime_to_str(
            self.post_3.created_at
        )
        params = {
            'from_date': date,
            'to_date': date,
        }
        response = self.client.get(self.url, params)
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

    def test_list_filter_period_included(self):
        from_date = self.datetime_to_str(
            self.post_3.created_at - timedelta(days=1)
        )
        to_date = self.datetime_to_str(
            self.post_3.created_at + timedelta(days=1)
        )
        params = {
            'from_date': from_date,
            'to_date': to_date
        }
        response = self.client.get(self.url, params)
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

    def test_list_filter_period_not_included(self):
        from_date = self.datetime_to_str(
            self.post_3.created_at + timedelta(days=1)
        )
        to_date = self.datetime_to_str(
            self.post_3.created_at + timedelta(days=2)
        )
        params = {
            'from_date': from_date,
            'to_date': to_date
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_from_date_bigger_than_to_date(self):
        from_date = self.datetime_to_str(
            self.post_3.created_at + timedelta(days=1)
        )
        to_date = self.datetime_to_str(
            self.post_3.created_at - timedelta(days=2)
        )
        params = {
            'from_date': from_date,
            'to_date': to_date
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class APIListFilterFailsTest(APITestCase):
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
        self.post_1 = PostService.create(
            self.user.username,
            'content1'
        )
        self.post_2 = PostService.create(
            self.user.username,
            'content2'
        )
        self.post_3 = PostService.create(
            self.user_2.username,
            'content3'
        )

    def test_list_filter_bad_author(self):
        params = {
            'author_id': 'id'
        }
        response = self.client.get(self.url, params)
        self.assertContains(
            response, 'author_id', status_code=status.HTTP_400_BAD_REQUEST
        )
        self.assertContains(
            response, 'number.', status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_list_filter_bad_from_date(self):
        params = {
            'from_date': '2024/01/01'
        }
        response = self.client.get(self.url, params)
        self.assertContains(
            response, 'from_date', status_code=status.HTTP_400_BAD_REQUEST
        )
        self.assertContains(
            response, 'valid date', status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_list_filter_bad_to_date(self):
        params = {
            'to_date': '2024/01/01'
        }
        response = self.client.get(self.url, params)
        self.assertContains(
            response, 'to_date', status_code=status.HTTP_400_BAD_REQUEST
        )
        self.assertContains(
            response, 'valid date', status_code=status.HTTP_400_BAD_REQUEST
        )
