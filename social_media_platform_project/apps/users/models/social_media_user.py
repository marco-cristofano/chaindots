from django.db import models
from utils.models.soft_delete import SoftDeleteModel
from django.contrib.auth.models import AbstractUser


class SocialMediaUser(SoftDeleteModel, AbstractUser):
    user_model_manager = AbstractUser._default_manager
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
