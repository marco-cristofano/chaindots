from django.test import TestCase
from apps.posts.services.post import PostService
from apps.posts.services.post import Post
from apps.users.services.social_media_user import SocialMediaUserService


class PostServiceTest(TestCase):
    def test_create(self):
        sm_user = SocialMediaUserService.create(
            username='username',
            email='email@email.com',
            password='password'
        )
        post = PostService.create(sm_user.user.email, 'content')
        self.assertEqual(post.author.user.username, 'username')
        self.assertEqual(post.author.user.email, 'email@email.com')
        self.assertEqual(post.content, 'content')
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.author.user.username, 'username')
        self.assertEqual(post.author.user.email, 'email@email.com')
        self.assertEqual(post.content, 'content')
