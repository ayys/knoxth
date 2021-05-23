"""
Serializers for knoxth models
"""

from knox.models import AuthToken
from knox.serializers import UserSerializer
from rest_framework import exceptions as drf_exceptions, serializers

from knoxth.fields import ContextField, PermissionsListField
from knoxth.models import Context, Scope


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

    context = ContextField()
    permissions_set = PermissionsListField()

    def create(self, validated_data):
        context = validated_data.get("context")
        permissions = validated_data.get("permissions_set")
        permissions_int = Scope.permissions_set_to_int(permissions)
        return Scope.objects.create(context=context, permissions=permissions_int)

    class Meta:
        model = Scope
        fields = ["context", "permissions_set"]


class AccessTokenSerializer(serializers.ModelSerializer):
    """
    Serializes Knox Token Class `knox.models.AuthToken
    """

    user = UserSerializer()

    class Meta:
        model = AuthToken
        fields = ["user", "created", "expiry"]


class TokenResponseSerializer(serializers.Serializer):
    """
    Take a list of context, permission JSON and convert it into a list of these
    Example input -
        [{ "context": "employees", "permissions": ["access"] }]
    """

    name = serializers.CharField()
    scopes = ScopeSerializer(many=True)

    def create(self, validated_data):
        """
        Create a new AuthToken with claim based the specified scope
        For this to work, save must be called with user=request.user
        """
        user = validated_data.get("user")
        if user is None:
            raise serializers.ValidationError(
                f"Pass the user argument when calling save() \
on {self.__class__.__name__} serializer"
            )
        name = validated_data.get("name")
        scopes = validated_data.get("scopes")
        token_obj, token = AuthToken.objects.create(user)
        claim = token_obj.claim
        claim.name = name
        claim.save()
        for scope in scopes:
            scope_ser = ScopeSerializer(data=scope)
            if scope_ser.is_valid():
                scope_obj = scope_ser.save()
                claim.scopes.add(scope_obj)
        return token_obj, token

    def update(self, instance, validated_data):
        raise drf_exceptions.NotAcceptable("Tokens cannot be updated!")
