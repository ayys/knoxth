"""
contains IsScoped which is a permission class that uses scopes
assigned to knox tokens for authorization
"""

from knox.models import AuthToken
from knox.settings import CONSTANTS
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import SAFE_METHODS, BasePermission

from knoxth.constants import ACCESS, DELETE, MODIFY


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
        return bool(
            auth_token
            and (
                (request.method in SAFE_METHODS and auth_token.claim.verify(IsScoped.context, ACCESS))
                or ((request.method == "POST" or request.method == "PUT") and auth_token.claim.verify(IsScoped.context, MODIFY))
                or ((request.method == "DELETE") and auth_token.claim.verify(IsScoped.context, DELETE))
            )
        )

    @staticmethod
    def get_auth_token(request, token_too=False):
        """
        Returns the Knox AuthToken object for given request.
        if token_too is True, returns a tuple (AuthToken Obj, Token String)
        """
        auth = get_authorization_header(request).split()
        if len(auth) == 2:
            authtoken = IsScoped.token_to_authtoken(auth[1])
            return (authtoken, auth[1]) if token_too else authtoken
        return None

    @staticmethod
    def token_to_authtoken(token: bytes):
        """
        Take token bytes from request header and output AuthToken object
        """
        token = token.decode("UTF-8")
        token_key = token[: CONSTANTS.TOKEN_KEY_LENGTH]
        authtoken = AuthToken.objects.get(token_key=str(token_key))
        return authtoken
