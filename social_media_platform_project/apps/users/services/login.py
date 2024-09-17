from typing import Dict
from django.contrib.auth import authenticate
from apps.users.services.authtoken import AuthTokenService


class LoginService:

    @classmethod
    def login(cls, username: str, password: str) -> Dict:
        print(username, password)
        from django.contrib.auth.models import User
        print(User.objects.filter(username=username).values('is_staff'))
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            return 
        token = AuthTokenService.get_token(user)
        return {'token': token.key}
