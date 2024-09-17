from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from apps.users.services.social_media_user import SocialMediaUserService


class CustomAPITestCase(APITestCase):

    def setUp(self):
        user = SocialMediaUserService.create(
            username='test_user',
            password='test_password',
            email='test_user@email.com'
        )
        Token.objects.get_or_create(user=user)
        self.client.force_authenticate(user=user)
