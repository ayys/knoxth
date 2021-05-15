"""
Views for knoxth

from knoxth.views import ContextViewSet
from knxoth.views import KnoxthLoginView
"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import (
    TokenAuthentication as DRFTokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knoxth.models import Context
from knoxth.serializers import (
    AccessTokenSerializer,
    ContextSerializer,
    ScopeSerializer,
    TokenResponseSerializer,
)


class ContextViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """

    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [IsAuthenticated]


class KnoxthLoginView(KnoxLoginView):
    """
    The Login view has to be authenticated with the authorization code
    acquired via DRF.
    """

    authentication_classes = [DRFTokenAuthentication]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create a DRF Token everytime the user object is updated.
    """
    Token.objects.filter(user=instance).delete()
    Token.objects.create(user=instance)


class AuthTokenViewset(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenResponseSerializer

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = AccessTokenSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        auth_tokens = AuthToken.objects.filter(user=self.request.user)
        return auth_tokens
