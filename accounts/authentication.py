import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class DapplesoftJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token type")
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header")

        try:
            payload = jwt.decode(
                token,
                settings.DAP_AUTH_PUBLIC_KEY,
                algorithms=["RS256"],
                options={"verify_aud": False},
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        email = payload.get("email")
        username = payload.get("username", email)
        role = payload.get("role")

        if not email:
            raise AuthenticationFailed("Invalid token payload")

        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        if hasattr(user, "role") and role:
            user.role = role
            user.save()

        return (user, None)
