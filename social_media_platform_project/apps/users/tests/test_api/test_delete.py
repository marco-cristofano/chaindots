from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.services.social_media_user import SocialMediaUserService


class APIDeleteUserTest(APITestCase):
    url = '/api/users/'

    def setUp(self):
        self.user_1 = SocialMediaUserService.create(
            username='username1',
            email='email1@email.com',
            password='password'
        )

    @classmethod
    def get_url(cls, pk):
        return cls.url + str(pk) + '/'

    def test_method_not_allowed(self):
        url = self.get_url(self.user_1.id)
        response = self.client.delete(url, {})
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
