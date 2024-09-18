from django.db import models
from apps.users.models import SocialMediaUser


class Post(models.Model):
    author = models.ForeignKey(
        SocialMediaUser,
        on_delete=models.CASCADE,
        related_name='posts')
    content = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self) -> str:
        return "{} ({})".format(self.author.email, self.id)
