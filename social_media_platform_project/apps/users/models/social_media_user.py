from django.db import models
from django.contrib.auth.models import AbstractUser


class SocialMediaUser(AbstractUser):
    followed = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers'
    )

    class Meta:
        verbose_name = 'SocialMediaUser'
        verbose_name_plural = 'SocialMediaUsers'

    def __str__(self) -> str:
        return self.email
