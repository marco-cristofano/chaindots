from django.db import models
from django.contrib.auth.models import User
from utils.models.soft_delete import SoftDeleteModel


class SocialMediaUser(SoftDeleteModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='social_media_user')  # TODO
    followed = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers'
    )

    def __str__(self) -> str:
        return self.user.email
