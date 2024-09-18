from utils.exists_or_404 import exists_object_or_404

from drf_spectacular.utils import extend_schema
from rest_framework import (
    status,
    permissions,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.users.models import SocialMediaUser

from apps.users.documentation import social_media_user as DOC
from apps.users.serializers.social_media_user import (
    SocialMediaUserCreateSerializer,
    SocialMediaUserDetailedSerializer,
    SocialMediaUserSerializer
)
from apps.users.services.social_media_user import SocialMediaUserService


class SocialMediaUserViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = SocialMediaUser.objects.order_by('email')
    serializer_class = SocialMediaUserSerializer
    detailed_serializer_class = SocialMediaUserDetailedSerializer
    create_serializer_class = SocialMediaUserCreateSerializer
    http_method_names = ['get', 'post']

    @extend_schema(**DOC.doc_user_list)
    def list(self, request):
        return super().list(request)

    @extend_schema(**DOC.doc_user_retrieve)
    def retrieve(self, request, pk=None):
        exists_object_or_404(SocialMediaUser, pk)
        user = SocialMediaUserService.detailed(pk)
        serializer = self.detailed_serializer_class(user)
        return Response(serializer.data)

    @extend_schema(**DOC.doc_user_create)
    def create(self, request, *args, **kwargs):
        serializer = self.create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = SocialMediaUserService.create(**serializer.validated_data)
        serializer_out = self.serializer_class(user)
        return Response(serializer_out.data, status=status.HTTP_201_CREATED)

    @extend_schema(**DOC.doc_add_follow)
    @action(detail=True, methods=['post'], url_path='follow/(?P<user_to_follow_pk>[^/.]+)')
    def add_follow(self, request, pk=None, user_to_follow_pk=None):
        exists_object_or_404(SocialMediaUser, pk)
        exists_object_or_404(SocialMediaUser, user_to_follow_pk)
        SocialMediaUserService.add_follow(pk, user_to_follow_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
