from rest_framework.test import APITestCase
from apps.users.services.social_media_user import SocialMediaUserService
from apps.posts.services.post import PostService
from apps.posts.services.comment import CommentService


class APIRetrieveUserPostAndCommentsTest(APITestCase):
    url = '/api/users/'

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

    @classmethod
    def get_url(cls, pk):
        return cls.url + str(pk) + '/'

    def test_retrieve_zero_posts_and_comments(self):
        url = self.get_url(self.user_1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user_1.id)
        self.assertEqual(user['username'], 'username1')
        self.assertEqual(user['email'], 'email1@email.com')
        self.assertEqual(user['total_posts'], 0)
        self.assertEqual(user['total_comments'], 0)

    def test_retrieve_two_posts_and_comments(self):
        post_1 = PostService.create(self.user_1.user.email, 'content1')
        post_2 = PostService.create(self.user_1.user.email, 'content2')
        CommentService.create(self.user_1.user.email, post_1, 'connent1')
        CommentService.create(self.user_1.user.email, post_2, 'connent2')

        url = self.get_url(self.user_1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user_1.id)
        self.assertEqual(user['username'], 'username1')
        self.assertEqual(user['email'], 'email1@email.com')
        self.assertEqual(user['total_posts'], 2)
        self.assertEqual(user['total_comments'], 2)

    def test_retrieve_two_posts_and_comments_in_another_user(self):
        post_1 = PostService.create(self.user_1.user.email, 'content1')
        post_2 = PostService.create(self.user_1.user.email, 'content2')
        CommentService.create(self.user_1.user.email, post_1, 'connent1')
        CommentService.create(self.user_1.user.email, post_2, 'connent2')

        url = self.get_url(self.user_2.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user_2.id)
        self.assertEqual(user['username'], 'username2')
        self.assertEqual(user['email'], 'email2@email.com')
        self.assertEqual(user['total_posts'], 0)
        self.assertEqual(user['total_comments'], 0)


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
    def get_url(cls, pk):
        return cls.url + str(pk) + '/'

    def test_zero_followed_and_followers(self):
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)

        url = self.get_url(self.single_user.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.single_user.id)
        self.assertEqual(user['username'], 'single_userername')
        self.assertEqual(user['email'], 'single_user@email.com')
        self.assertEqual(len(response.data['followed']), 0)
        self.assertEqual(len(response.data['followers']), 0)

    def test_one_followed(self):
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)

        url = self.get_url(self.user.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user.id)
        self.assertEqual(user['username'], 'username')
        self.assertEqual(user['email'], 'email@email.com')
        self.assertEqual(len(response.data['followed']), 1)
        followed = response.data['followed'][0]
        self.assertEqual(followed['id'], self.user_to_follow.id)
        self.assertEqual(followed['username'], 'user_to_follow')
        self.assertEqual(followed['email'], 'user_to_follow@email.com')
        self.assertEqual(len(response.data['followers']), 0)

    def test_one_follower(self):
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)

        url = self.get_url(self.user_to_follow.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user_to_follow.id)
        self.assertEqual(user['username'], 'user_to_follow')
        self.assertEqual(user['email'], 'user_to_follow@email.com')
        self.assertEqual(len(response.data['followers']), 1)
        follower = response.data['followers'][0]
        self.assertEqual(follower['id'], self.user.id)
        self.assertEqual(follower['username'], 'username')
        self.assertEqual(follower['email'], 'email@email.com')
        self.assertEqual(len(response.data['followed']), 0)

    def test_double_followed(self):
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)

        url = self.get_url(self.user.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user.id)
        self.assertEqual(user['username'], 'username')
        self.assertEqual(user['email'], 'email@email.com')
        self.assertEqual(len(response.data['followed']), 1)
        followed = response.data['followed'][0]
        self.assertEqual(followed['id'], self.user_to_follow.id)
        self.assertEqual(followed['username'], 'user_to_follow')
        self.assertEqual(followed['email'], 'user_to_follow@email.com')
        self.assertEqual(len(response.data['followers']), 0)

    def test_double_followers(self):
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)

        url = self.get_url(self.user_to_follow.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user_to_follow.id)
        self.assertEqual(user['username'], 'user_to_follow')
        self.assertEqual(user['email'], 'user_to_follow@email.com')
        self.assertEqual(len(response.data['followers']), 1)
        follower = response.data['followers'][0]
        self.assertEqual(follower['id'], self.user.id)
        self.assertEqual(follower['username'], 'username')
        self.assertEqual(follower['email'], 'email@email.com')
        self.assertEqual(len(response.data['followed']), 0)

    def test_followed_and_simultaneous_follower(self):
        SocialMediaUserService.add_follow(self.user, self.user_to_follow)
        SocialMediaUserService.add_follow(self.user_to_follow, self.user)

        url = self.get_url(self.user_to_follow.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        user = response.data
        self.assertEqual(user['id'], self.user_to_follow.id)
        self.assertEqual(user['username'], 'user_to_follow')
        self.assertEqual(user['email'], 'user_to_follow@email.com')
        self.assertEqual(len(response.data['followers']), 1)
        follower = response.data['followers'][0]
        self.assertEqual(follower['id'], self.user.id)
        self.assertEqual(follower['username'], 'username')
        self.assertEqual(follower['email'], 'email@email.com')
        self.assertEqual(len(response.data['followed']), 1)
        followed = response.data['followers'][0]
        self.assertEqual(followed['id'], self.user.id)
        self.assertEqual(followed['username'], 'username')
        self.assertEqual(follower['email'], 'email@email.com')
