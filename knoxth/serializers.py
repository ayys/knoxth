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

