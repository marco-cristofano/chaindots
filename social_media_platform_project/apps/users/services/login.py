from typing import Dict
from django.contrib.auth import authenticate
from apps.users.services.authtoken import AuthTokenService
from rest_framework.exceptions import AuthenticationFailed


class LoginService:

    @classmethod
    def login(cls, username: str, password: str) -> Dict:
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed()
        token = AuthTokenService.get_token(user)
        return {'token': token.key}
