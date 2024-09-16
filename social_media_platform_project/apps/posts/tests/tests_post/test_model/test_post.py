from django.test import TestCase
from apps.users.services.social_media_user import SocialMediaUserService
from apps.posts.services.post import PostService


class PostTest(TestCase):
    def setUp(self):
        SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        self.post = PostService.create('email@email.com', 'content')

    def test_str(self):
        str_format = "email@email.com ({})".format(self.post.id)
        self.assertEqual(str(self.post), str_format)
