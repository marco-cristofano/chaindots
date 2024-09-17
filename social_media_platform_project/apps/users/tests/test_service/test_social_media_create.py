from django.test import TestCase
from apps.users.services.social_media_user import SocialMediaUserService
from apps.users.models.social_media_user import SocialMediaUser


class SocialMedialServiceCreateTest(TestCase):
    def test_create(self):
        sm_user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        self.assertEqual(sm_user.username, 'username')
        self.assertEqual(sm_user.email, 'email@email.com')
        self.assertIsNotNone(sm_user.password)
        sm_user = SocialMediaUser.objects.get(email='email@email.com')
        self.assertEqual(sm_user.username, 'username')
        self.assertEqual(sm_user.email, 'email@email.com')
        self.assertIsNotNone(sm_user.password)
