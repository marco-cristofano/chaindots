from rest_framework import routers

from apps.posts.api.post import PostViewset
from apps.users.api.social_media_user import SocialMediaUserViewset

app_name = 'api'
router = routers.SimpleRouter()
router.register(r'posts', PostViewset)
router.register(r'users', SocialMediaUserViewset)
urlpatterns = router.urls
