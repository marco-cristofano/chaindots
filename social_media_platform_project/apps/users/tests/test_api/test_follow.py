from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.services.social_media_user import SocialMediaUserService


class APIRetrieveUserFollowedAndFollowersTest(APITestCase):
    url = '/api/users/'

    def setUp(self):
        self.user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        self.user_to_follow = SocialMediaUserService.create(
            username='user_to_follow',
            email='user_to_follow@email.com',
            password='password'
        )
        self.single_user = SocialMediaUserService.create(
            username='single_userername',
            email='single_user@email.com',
            password='password'
        )

    @classmethod
    def get_url(cls, pk_user, pk_user_to_follow):
        return "{}{}/follow/{}/".format(cls.url, pk_user, pk_user_to_follow)

    def test_add_follow(self):
        url = self.get_url(self.user.id, self.user_to_follow.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.followed.count(), 1)
        self.assertEqual(self.user.followers.count(), 0)
        self.user_to_follow.refresh_from_db()
        self.assertEqual(self.user_to_follow.followed.count(), 0)
        self.assertEqual(self.user_to_follow.followers.count(), 1)

    def test_fail_user_pk(self):
        url = self.get_url(100, self.user_to_follow.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_user_to_follow_pk(self):
        url = self.get_url(self.user.id, 100)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
