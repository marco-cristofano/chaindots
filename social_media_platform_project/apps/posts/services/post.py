from apps.posts.models import Post
from apps.users.models import SocialMediaUser


class PostService:

    @classmethod
    def create(cls, author_email: str, content: str):
        """Creates a new post.

        Args:
            author (SocialMediaUser): author email of post
            content (str): content of post

        Returns:
            Post: New post
        """
        sm_user = SocialMediaUser.objects.get(user__email=author_email)
        post = Post.objects.create(
            author=sm_user,
            content=content
        )
        return post
