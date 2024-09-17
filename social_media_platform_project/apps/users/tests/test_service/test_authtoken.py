from django.test import TestCase
from rest_framework.authtoken.models import Token
from apps.users.services.social_media_user import SocialMediaUserService
from apps.users.services.authtoken import AuthTokenService


class AuthTokenServiceTest(TestCase):
    def test_create_token(self):
        sm_user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        AuthTokenService.create_token(sm_user)
        self.assertTrue(Token.objects.filter(user=sm_user).exists())

    def test_get_token(self):
        sm_user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        AuthTokenService.create_token(sm_user)
        self.assertIsNotNone(AuthTokenService.get_token(user=sm_user))
