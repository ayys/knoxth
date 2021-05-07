from django.core.exceptions import ObjectDoesNotExist
from knox.models import AuthToken
from knox.settings import CONSTANTS
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import SAFE_METHODS, BasePermission

from knoxth.constants import ACCESS, DELETE, MODIFY
from knoxth.models import Claim


class IsScoped(BasePermission):
    """
    The request is authorized based on token,
    or is a read-only request.
    """
    def has_permission(self, request, view):
        auth_token = self.get_auth_token(request)
        print(ACCESS, IsScoped.context,
              auth_token.claim,
              auth_token.claim.verify(IsScoped.context, ACCESS))
        return bool(
            auth_token and
            ((request.method in SAFE_METHODS and
              auth_token.claim.verify(IsScoped.context, ACCESS)) or
             ((request.method == 'POST') and
              auth_token.claim.verify(IsScoped.context, MODIFY)) or
             ((request.method == 'DELETE') and
              auth_token.claim.verify(IsScoped.context, DELETE)))
        )

    def get_auth_token(self, request):
        auth = get_authorization_header(request).split()
        if len(auth) == 2:
            token = auth[1].decode("UTF-8")
            token_key = token[:CONSTANTS.TOKEN_KEY_LENGTH]
            authtoken = AuthToken.objects.get(token_key=str(token_key))
            try:
                # try to access the token claim
                authtoken.claim
            except ObjectDoesNotExist:
                # if the claim does not exist, it's probably a login token
                # So lets not add any scopes, just incase ;)
                Claim.objects.create(token=authtoken)
            return authtoken
        return None
