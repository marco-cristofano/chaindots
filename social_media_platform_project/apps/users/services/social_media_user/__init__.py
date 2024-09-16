from django.contrib.auth.models import User
from django.db.models import Count
from apps.users.models import SocialMediaUser


class SocialMediaUserService:
    model = SocialMediaUser

    @classmethod
    def create(cls, username: str, email: str, password: str):
        """Creates a new social media user.

        Args:
            username (str): username of social media user
            email (str): email of social media user
            password (str): password of social media user

        Returns:
            SocialMediaUser: New social media user
        """
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        sm_user = cls.model.objects.create(user=user)
        return sm_user

    @classmethod
    def add_follow(
                cls, user: SocialMediaUser, user_to_follow: SocialMediaUser
            ) -> None:
        """Adds user to follow.

        Args:
            user (SocialMediaUser): id of user
            user_to_follow (SocialMediaUser): id of user to follow
        """
        user.followed.add(user_to_follow)
        user.save()

    @classmethod
    def detailed(cls, social_media_user_id: int) -> SocialMediaUser:
        """Returns detailed social media user.

        Args:
            social_media_user_id (int): id of social media user

        Returns:
            SocialMediaUser: Insance of social media user
        """
        cls.model.objects.get(id=social_media_user_id).posts.all()
        user = cls.model.objects.filter(
            id=social_media_user_id
        ).prefetch_related(
            'followed',
            'followers'
        ).annotate(
            total_posts=Count('posts', distinct=True),
            total_comments=Count('comments', distinct=True)
        ).get()
        return user
