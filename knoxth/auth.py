"""
contains IsScoped which is a permission class that uses scopes
assigned to knox tokens for authorization
"""

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
        """
        this method is called to check if the request has
        necessary permissions to authorize access.
        It checks if the current token claim can be used to
        verify the scope permission for requested context
        """
        auth_token = IsScoped.get_auth_token(request)
        if auth_token is None:
            return False
        print(
            ACCESS,
            IsScoped.context,
            auth_token.claim,
            auth_token.claim.verify(IsScoped.context, ACCESS),
        )
        return bool(
            auth_token
            and (
                (
                    request.method in SAFE_METHODS
                    and auth_token.claim.verify(IsScoped.context, ACCESS)
                )
                or (
                    (request.method == "POST")
                    and auth_token.claim.verify(IsScoped.context, MODIFY)
                )
                or (
                    (request.method == "DELETE")
                    and auth_token.claim.verify(IsScoped.context, DELETE)
                )
            )
        )

    @staticmethod
    def get_auth_token(request):
        """
        Returns the Knox AuthToken object for given request.
        """
        auth = get_authorization_header(request).split()
        if len(auth) == 2:
            return IsScoped.token_to_authtoken(auth[1])
        return None

    @staticmethod
    def token_to_authtoken(token: bytes):
        """
        Take token bytes from request header and output AuthToken object
        """
        token = token.decode("UTF-8")
        token_key = token[: CONSTANTS.TOKEN_KEY_LENGTH]
        authtoken = AuthToken.objects.get(token_key=str(token_key))
        try:
            # try to access the token claim
            authtoken.claim
        except ObjectDoesNotExist:
            # if the claim does not exist, it's probably a login token
            # So lets not add any scopes, just incase ;)
            Claim.objects.create(token=authtoken)
        return authtoken
