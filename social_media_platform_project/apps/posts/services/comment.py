from apps.posts.models import Post
from apps.users.models import SocialMediaUser
from apps.posts.models.comment import Comment


class CommentService:

    @classmethod
    def create(cls, author_username: str, post: Post, comment: str):
        """Creates a new comment.

        Args:
            author_username (str): username of comment author
            post (Post): post of comment
            comment (str): content of comment

        Returns:
            Comment: New comment
        """
        sm_user = SocialMediaUser.objects.get(username=author_username)
        comment = Comment.objects.create(
            author=sm_user,
            post=post,
            comment=comment
        )
        return comment
