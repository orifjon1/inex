from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework_simplejwt.tokens import AccessToken, TokenError

# User = get_user_model()


class WebSocketJWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            token = JWTAuthentication().get_validated_token(scope["query_string"].decode("utf-8"))
        except InvalidToken as e:
            print(f"Invalid token: {e}")
            return None
        except TokenError as e:
            print(f"Token error: {e}")
            return None

        user_id = token["user_id"]
        user = await self.get_user(user_id)

        if user is None:
            print("User not found")
            return None

        scope['user'] = user

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return None

# @database_sync_to_async
# def get_user(user_id):
#     return User.objects.get(id=user_id)
#
#
# class WebSocketJWTAuthMiddleware:
#
#     def __init__(self, app):
#         self.app = app
#
#     async def __call__(self, scope, receive, send):
#         parsed_query_string = parse_qs(scope["query_string"])
#         token = parsed_query_string.get(b"token")[0].decode("utf-8")
#
#         access_token = AccessToken(token)
#         scope["user"] = await get_user(access_token["user_id"])
#
#         return await self.app(scope, receive, send)
