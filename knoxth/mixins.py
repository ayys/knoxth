"""
This module contains mixins for tokens. There are four mixins

* Create Token Mixin - Mixin that implements methods to create token
* Delete Token Mixin - Mixin that implements methods to destroy token
* Refresh Token Mixin - Mixin that implements methods to refresh token
* List Token Mixin - Mixin that implements methods to list tokens
"""
from rest_framework import mixins, status
from rest_framework.response import Response

from knoxth.auth import IsScoped
from knoxth.serializers import AccessTokenSerializer, ScopeSerializer


class CreateTokenMixin(mixins.CreateModelMixin):
    """
    Create and return a token when given proper input
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_obj, token = serializer.save(user=self.request.user)
        token_serializer = AccessTokenSerializer(token_obj)
        scopes = ScopeSerializer(token_obj.claim.scopes.all(), many=True)
        data = token_serializer.data
        data.update({"token": token})
        data.update({"scopes": scopes.data})
        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )


class DestroyTokenMixin(mixins.DestroyModelMixin):
    """
    Destroy tokens with proper input
    """

    def destroy(self, request, *args, **kwargs):
        authtoken, token = IsScoped.get_auth_token(request, token_too=True)
        if request.user.auth_token_set.filter(id=authtoken.id).exists():
            authtoken.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={
                "token": token,
                "error": "You do not have proper authorization to delete this token",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ListTokensMixin(mixins.ListModelMixin):
    """
    List all the tokens for the user
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = AccessTokenSerializer(queryset, many=True)
        return Response(serializer.data)
