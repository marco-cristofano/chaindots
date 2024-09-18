from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AuthTokenService:
    @classmethod
    def create_token(cls, user: User) -> Token:
        token = Token.objects.get_or_create(user=user)[0]
        return token

    @classmethod
    def get_token(cls, user: User) -> Token:
        token = Token.objects.get(user=user)
        return token
