'''
Serializers for knoxth models
'''

from rest_framework.serializers import ModelSerializer, ReadOnlyField

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
        fields = ['name']
