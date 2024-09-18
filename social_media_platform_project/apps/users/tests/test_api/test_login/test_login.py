from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.services.social_media_user import SocialMediaUserService


class APILoginTest(APITestCase):
    url = '/login/'

    def setUp(self):
        self.user = SocialMediaUserService.create(
            username='test_user',
            password='test_password',
            email='test_user@email.com'
        )

    def test_login_success(self):
        credentials = {
            'username': self.user.username,
            'password': 'test_password'
        }
        response = self.client.post(self.url, credentials)
        self.assertContains(
            response, 'token', 1, status_code=status.HTTP_201_CREATED
        )

    def test_login_bad_credentials(self):
        credentials = {
            'username': self.user.username,
            'password': 'bad'
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_password(self):
        credentials = {
            'username': self.user.username,
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_username(self):
        credentials = {
            'password': 'bad'
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
