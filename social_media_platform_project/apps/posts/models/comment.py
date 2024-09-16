from django.db import models
from apps.posts.models.post import Post
from apps.users.models import SocialMediaUser
from utils.models.soft_delete import SoftDeleteModel


class Comment(SoftDeleteModel):
    author = models.ForeignKey(
        SocialMediaUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "{} ({})".format(self.author.user.email, self.id)
