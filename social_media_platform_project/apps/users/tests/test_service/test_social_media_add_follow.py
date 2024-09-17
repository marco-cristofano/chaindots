from django.test import TestCase
from apps.users.services.social_media_user import SocialMediaUserService
from apps.users.models.social_media_user import SocialMediaUser


class SocialMedialServiceAddFollowTest(TestCase):
    def test_add_follow(self):
        sm_user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        sm_user_to_follow = SocialMediaUserService.create(
            username='username_to_follow',
            email='username_to_follow@email.com',
            password='password'
        )

        SocialMediaUserService.add_follow(
            sm_user.id,
            sm_user_to_follow.id
        )
        self.assertEqual(sm_user.followed.count(), 1)
        self.assertEqual(sm_user.followers.count(), 0)
        self.assertEqual(sm_user_to_follow.followed.count(), 0)
        self.assertEqual(sm_user_to_follow.followers.count(), 1)
