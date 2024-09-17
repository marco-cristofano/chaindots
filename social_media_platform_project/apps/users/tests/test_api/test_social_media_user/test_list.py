from rest_framework import status
from utils.tests.apt_test import CustomAPITestCase as APITestCase
from apps.users.services.social_media_user import SocialMediaUserService


class APIListUserTest(APITestCase):
    url = '/api/users/'

    def setUp(self):
        super().setUp()
        self.user_1 = SocialMediaUserService.create(
            username='username1',
            email='email1@email.com',
            password='password'
        )
        self.user_2 = SocialMediaUserService.create(
            username='username2',
            email='email2@email.com',
            password='password'
        )
        self.user_3 = SocialMediaUserService.create(
            username='username3',
            email='email3@email.com',
            password='password'
        )

    def test_list_with_order(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        user = response.data[0]
        self.assertEqual(user['username'], 'username1')
        self.assertEqual(user['email'], 'email1@email.com')
        self.assertEqual(user['id'], self.user_1.id)
        user = response.data[1]
        self.assertEqual(user['username'], 'username2')
        self.assertEqual(user['email'], 'email2@email.com')
        self.assertEqual(user['id'], self.user_2.id)
        user = response.data[2]
        self.assertEqual(user['username'], 'username3')
        self.assertEqual(user['email'], 'email3@email.com')
        self.assertEqual(user['id'], self.user_3.id)
