"""
Serializers for knoxth models
"""

import functools

from knox.models import AuthToken
from rest_framework import exceptions as drf_exceptions, serializers

from knoxth.constants import ACCESS, DELETE, MODIFY
from knoxth.models import Claim, Context, Scope


class ContextSerializer(serializers.ModelSerializer):
    """
    Serializes the Context model and exposes it's name property
    """

    class Meta:
        """
        Only expose the name field for Context Model because
        that is the only field available
        """

        model = Context
        fields = ["name"]


class ScopeSerializer(serializers.ModelSerializer):
    """
    Serializes knoxth Scopes with field - context:str , permissions: [str...]
    """

    class Meta:
        model = Scope
        fields = ["context", "permissions_set"]
        read_only_fields = ["pk", "context", "permissions_set"]


class AccessTokenSerializer(serializers.ModelSerializer):
    """
    Serializes Knox Token Class `knox.models.AuthToken
    """

    class Meta:
        model = AuthToken
        fields = ["user", "created", "expiry", "user"]


class TokenResponseSerializer(serializers.Serializer):
    """
    Take a list of context, permission JSON and convert it into a list of these
    Example input -
        { "context": "employees", "permissions": ["access"] }
    """

    context = serializers.CharField(max_length=255, read_only=True)
    permissions = serializers.ListField(
        child=serializers.RegexField(r"access|modify|delete", default="access"),
        required=True,
        max_length=3,
    )

    def reduce_perms_to_int(self, perms=None):
        """
        Convert the permission strings to integer
        """
        perms = self.permissions if perms is None else perms
        perm_ints = map(
            lambda perm: ACCESS
            if perm.lower() == "access"
            else MODIFY
            if perm.lower() == "modify"
            else DELETE
            if perm.lower() == "delete"
            else 0,
            perms,
        )
        return functools.reduce(lambda p1, p2: p1 | p2, perm_ints)

    def create(self, validated_data):
        """
        Create a new AuthToken with claim based the specified scope
        For this to work, save must be called with user=request.user
        """
        user = validated_data.get("user")
        if user is None:
            raise serializers.ValidationError(
                f"Pass the user argument when calling save()\
on {self.__class__.__name__} serializer"
            )
        context_name = validated_data.get("context")
        if Context.objects.filter(name=context_name).empty():
            raise serializers.ValidationError(
                f"Context Name `{context_name}` does not exist"
            )
        perms = validated_data.get("permissions")
        permissions = self.reduce_perms_to_int(perms)
        authtoken, token = AuthToken.objects.create(user=user)
        Claim.objects.create(token=authtoken)
        authtoken.claim.add_scope(context_name, permissions)
        return authtoken

    def update(self, instance, validated_data):
        raise drf_exceptions.NotAcceptable("Tokens cannot be updated!")
