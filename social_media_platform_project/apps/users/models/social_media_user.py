from django.db import models
from django.contrib.auth.models import User
from utils.models.soft_delete import SoftDeleteModel


class SocialMediaUser(SoftDeleteModel, User):
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
