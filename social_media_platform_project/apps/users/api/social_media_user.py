from rest_framework import viewsets
from rest_framework.response import Response
from apps.users.models import SocialMediaUser
from apps.users.serializers.social_media_user import (
    SocialMediaUserDetailedSerializer,
    SocialMediaUserSerializer
)
from apps.users.services.social_media_user import SocialMediaUserService


class SocialMediaUserViewset(viewsets.ModelViewSet):
    queryset = SocialMediaUser.objects.order_by('user__email')
    serializer_class = SocialMediaUserSerializer
    detailed_serializer_class = SocialMediaUserDetailedSerializer

    def retrieve(self, request, pk=None):
        user = self.get_object()  # TODO
        user = SocialMediaUserService.detailed(pk)
        serializer = self.detailed_serializer_class(user)
        return Response(serializer.data)
