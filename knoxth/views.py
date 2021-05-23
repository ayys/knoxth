"""
Views for knoxth

from knoxth.views import ContextViewSet
from knxoth.views import KnoxthLoginView
from knxoth.views import AuthTokenViewset
"""
from django.conf import settings
from django.contrib.auth.signals import user_logged_out
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status, views, viewsets
from rest_framework.authentication import (
    TokenAuthentication as DRFTokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knoxth import mixins
from knoxth.auth import IsScoped
from knoxth.models import Context
from knoxth.serializers import ContextSerializer, TokenResponseSerializer


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
    mixins.CreateTokenMixin,
    mixins.ListTokensMixin,
    mixins.DestroyTokenMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset that deals with authtoken stuff

    * create new token
    * delete token
    * list tokens for user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TokenResponseSerializer

    def get_queryset(self):
        auth_tokens = AuthToken.objects.filter(user=self.request.user)
        return auth_tokens


class AuthTokenRefresh(views.APIView):
    """
    Refresh AuthToken such that a new token is needed to authenticate
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TokenResponseSerializer

    def get(self, request, *args, **kwargs):
        """
        create a new authtoken object and copy its creds to old one
        """
        authtoken = IsScoped.get_auth_token(request)
        new_authtoken = AuthToken.objects.create(request.user)[0]
        for field in AuthToken._meta.fields:
            att = field.attname
            setattr(authtoken, att, getattr(new_authtoken, att))
        authtoken.save()
        new_authtoken.delete()


class LogoutAllExceptCurrentView(views.APIView):
    """
    Log the user out of all sessions except the current one
    I.E. deletes all auth tokens for the user except the token currently in use
    """

    def post(self, request, format=None):
        authtoken = IsScoped.get_auth_token(request)
        request.user.auth_token_set.filter(~Q(id=authtoken.id)).delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
