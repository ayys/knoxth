"""
Serializers for knoxth models
"""

from rest_framework.serializers import ModelSerializer

from knoxth.models import Context


class ContextSerializer(ModelSerializer):
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

