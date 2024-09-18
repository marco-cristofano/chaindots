from drf_spectacular.utils import extend_schema
from rest_framework import (
    permissions,
    status,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.documentation import login as DOC
from apps.users.serializers.login import LoginSerializer
from apps.users.services.login import LoginService


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(**DOC.doc_login)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        token = LoginService.login(params['username'], params['password'])
        return Response(token, status=status.HTTP_201_CREATED)
