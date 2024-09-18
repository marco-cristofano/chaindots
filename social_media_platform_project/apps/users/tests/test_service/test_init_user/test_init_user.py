from django.test import TestCase
from apps.users.models import SocialMediaUser
from apps.users.services.init_user import init_user


class CommentTest(TestCase):

    def test_create_user(self):
        init_user()
        self.assertTrue(
            SocialMediaUser.objects.filter(username='admin').exists()
        )

    def test_not_duplicate_user(self):
        init_user()
        init_user()
        self.assertEqual(
            SocialMediaUser.objects.filter(username='admin').count(),
            1
        )
