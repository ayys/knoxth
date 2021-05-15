from rest_framework.serializers import Field

from knoxth.models import Context


class PermissionsListField(Field):
    """
    Serializer Field for scope permissions
    """

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ContextField(Field):
    """
    Serializer Field for scope context
    """

    def to_internal_value(self, data):
        context_search = Context.objects.filter(name=data)
        return context_search.first() if context_search.exists() else None

    def to_representation(self, value):
        context_search = Context.objects.filter(name=value)
        context = context_search.first() if context_search.exists() else None
        if context is not None:
            return context.name
        return None
