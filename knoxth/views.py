"""
Views for knoxth

from knoxth.views import ContextViewSet
from knxoth.views import KnoxthLoginView
"""
import itertools

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import mixins, viewsets
from rest_framework.authentication import (
    TokenAuthentication as DRFTokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from knoxth.models import Claim, Context, Scope
from knoxth.serializers import ContextSerializer, ScopeSerializer


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
    serializer_class = ScopeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        auth_tokens = AuthToken.objects.filter(user=self.request.user)
        claims = Claim.objects.filter(token__in=auth_tokens)
        scope_pks = [[scope.pk for scope in claim.scopes.all()] for claim in claims]
        normalized_scope_pks = list(itertools.chain.from_iterable(scope_pks))
        return Scope.objects.filter(pk__in=normalized_scope_pks)
