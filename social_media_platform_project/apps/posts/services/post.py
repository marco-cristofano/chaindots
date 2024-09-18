from django.db.models import QuerySet

from apps.posts.models import (
    Comment,
    Post
)
from apps.users.models import SocialMediaUser


class PostService:
    model = Post

    @classmethod
    def create(cls, author_username: str, content: str):
        """Creates a new post.

        Args:
            author_username (str): author username of post
            content (str): content of post

        Returns:
            Post: New post
        """
        sm_user = SocialMediaUser.objects.get(username=author_username)
        post = cls.model.objects.create(
            author=sm_user,
            content=content
        )
        return post

    @classmethod
    def detailed(cls, post_id: int) -> Post:
        """Returns detailed post.

        Args:
            post_id (int): id of post
        Returns:
            Post: instance of post
        """
        user = cls.model.objects.filter(
            id=post_id
        ).select_related(
            'author',
        ).prefetch_related(
            'comments',
            'comments__author'
        ).get()
        return user

    @classmethod
    def get_all_comments(cls, post_id: int) -> QuerySet[Comment]:
        """Returns all comments of post.

        Args:
            post_id (int): id of post
        Returns:
            comments: queryset of comments
        """
        comments = Comment.objects.filter(
            post__id=post_id
        ).select_related(
            'author'
        ).order_by('-created_at')
        return comments
