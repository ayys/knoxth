from rest_framework.serializers import ModelSerializer, ReadOnlyField

from knoxth.models import Context


class ContextSerializer(ModelSerializer):
    class Meta:
        model = Context
        fields = ['name']
