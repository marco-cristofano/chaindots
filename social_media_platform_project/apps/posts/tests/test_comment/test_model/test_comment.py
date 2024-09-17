from django.test import TestCase
from apps.users.services.social_media_user import SocialMediaUserService
from apps.posts.services.post import PostService
from apps.posts.services.comment import CommentService


class CommentTest(TestCase):
    def setUp(self):
        SocialMediaUserService.create(
            username='username_comment_creator',
            email='username_comment_creator@email.com',
            password='password'
        )
        SocialMediaUserService.create(
            username='username_post_creator',
            email='username_post_creator@email.com',
            password='password'
        )
        post = PostService.create('username_post_creator', 'content')
        self.comment = CommentService.create(
            'username_comment_creator',
            post,
            'comment'
        )

    def test_str(self):
        str_format = "username_comment_creator@email.com ({})".format(
            self.comment.id
        )
        self.assertEqual(str(self.comment), str_format)
