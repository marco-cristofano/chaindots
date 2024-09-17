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

    def test_login(self):
        credentials = {
            'username': self.user.username,
            'password': 'test_password'
        }
        response = self.client.post(self.url, credentials)
        #print(response.data)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertContains(
        #    response, 'token', 1, status_code=status.HTTP_201_CREATED
        #)
