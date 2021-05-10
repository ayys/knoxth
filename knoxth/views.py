'''
Views for knoxth

from knoxth.views import ContextViewSet
from knxoth.views import KnoxthLoginView
'''

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from knox.views import LoginView as KnoxLoginView
from rest_framework import viewsets
from rest_framework.authentication import (
    TokenAuthentication as DRFTokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from knoxth.models import Context
from knoxth.serializers import ContextSerializer


class ContextViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [IsAuthenticated]


class KnoxthLoginView(KnoxLoginView):
    '''
    The Login view has to be authenticated with the authorization code
    acquired via DRF.
    '''
    authentication_classes = [DRFTokenAuthentication]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''
    Create a DRF Token everytime the user object is updated.
    '''
    try:
        instance.token.delete()
    except: pass
    Token.objects.create(user=instance)
