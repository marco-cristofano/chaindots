from rest_framework import routers

from apps.users.api.social_media_user import SocialMediaUserViewset

app_name = 'api'
router = routers.SimpleRouter()
router.register(r'users', SocialMediaUserViewset)
urlpatterns = router.urls
