from rest_framework import status
from utils.tests.apt_test import CustomAPITestCase as APITestCase
from apps.posts.services.post import PostService
from apps.users.services.social_media_user import SocialMediaUserService


class APIDeleteTest(APITestCase):
    url = '/api/posts/'

    def setUp(self):
        super().setUp()
        self.user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        self.post = PostService.create(
            self.user.username,
            'content'
        )

    def get_url(self, post_id):
        return "{}{}/".format(self.url, post_id)

    def test_method_not_allowed(self):
        url = self.get_url(self.post.id)
        response = self.client.delete(url, {})
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
