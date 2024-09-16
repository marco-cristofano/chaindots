from django.test import TestCase
from apps.users.services.social_media_user import SocialMediaUserService


class SocialMedialUserTest(TestCase):
    def test_str(self):
        sm_user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )

        self.assertEqual(str(sm_user), 'email@email.com')
