from django.test import TestCase
from apps.posts.services.comment import CommentService
from apps.posts.services.comment import Comment
from apps.posts.services.post import PostService
from apps.users.services.social_media_user import SocialMediaUserService


class PostServiceTest(TestCase):
    def test_create(self):
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
        comment = CommentService.create(
            author_username='username_comment_creator',
            post=post,
            comment='comment'
        )
        self.assertEqual(
            comment.author.username, 'username_comment_creator'
        )
        self.assertEqual(
            comment.author.email, 'username_comment_creator@email.com'
        )
        self.assertEqual(comment.comment, 'comment')
        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(
            comment.author.username, 'username_comment_creator'
        )
        self.assertEqual(
            comment.author.email, 'username_comment_creator@email.com'
        )
        self.assertEqual(comment.comment, 'comment')
