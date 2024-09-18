from django.db import models
from apps.users.models import SocialMediaUser
from apps.posts.models.post import Post


class Comment(models.Model):
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

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        return "{} ({})".format(self.author.email, self.id)
