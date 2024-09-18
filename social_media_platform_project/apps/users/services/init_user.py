from apps.users.models import SocialMediaUser
from apps.users.services.social_media_user import SocialMediaUserService


def init_user(*args, **kwargs):
    """function that creates an user
    """
    if not SocialMediaUser.objects.filter(username='admin').exists():
        SocialMediaUserService.create(
            username='admin',
            password='admin',
            email='admin@admin.com'
        )
