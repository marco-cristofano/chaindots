from django.test import TestCase
from apps.posts.services.comment import CommentService
from apps.posts.services.post import PostService
from apps.users.services.social_media_user import SocialMediaUserService


class SocialMedialServiceDetailedTest(TestCase):

    def setUp(self):
        self.user_1 = SocialMediaUserService.create(
            username='username1',
            email='email1@email.com',
            password='password'
        )
        self.user_2 = SocialMediaUserService.create(
            username='username2',
            email='email2@email.com',
            password='password'
        )

    def test_zero_posts_and_comments(self):
        sm_user = SocialMediaUserService.detailed(self.user_1.id)
        self.assertEqual(sm_user.id, self.user_1.id)
        self.assertEqual(sm_user.username, 'username1')
        self.assertEqual(sm_user.email, 'email1@email.com')
        self.assertEqual(sm_user.total_posts, 0)
        self.assertEqual(sm_user.total_comments, 0)

    def test_two_posts_and_comments(self):
        post_1 = PostService.create(self.user_1.username, 'content1')
        post_2 = PostService.create(self.user_1.username, 'content2')
        CommentService.create(self.user_1.username, post_1, 'connent1')
        CommentService.create(self.user_1.username, post_2, 'connent2')

        sm_user = SocialMediaUserService.detailed(self.user_1.id)
        self.assertEqual(sm_user.id, self.user_1.id)
        self.assertEqual(sm_user.username, 'username1')
        self.assertEqual(sm_user.email, 'email1@email.com')
        self.assertEqual(sm_user.total_posts, 2)
        self.assertEqual(sm_user.total_comments, 2)

    def test_two_posts_and_comments_in_another_user(self):
        post_1 = PostService.create(self.user_1.username, 'content1')
        post_2 = PostService.create(self.user_1.username, 'content2')
        CommentService.create(self.user_1.username, post_1, 'connent1')
        CommentService.create(self.user_1.username, post_2, 'connent2')

        sm_user = SocialMediaUserService.detailed(self.user_2.id)
        self.assertEqual(sm_user.id, self.user_2.id)
        self.assertEqual(sm_user.username, 'username2')
        self.assertEqual(sm_user.email, 'email2@email.com')
        self.assertEqual(sm_user.total_posts, 0)
        self.assertEqual(sm_user.total_comments, 0)
