"""
Implementation of `withContext` decorator.

from knoxth.decorators import withContext

This decorator does two things:
1. Injects a class property `context` to isScoped with the value equal to current context
2. Injects IsScoped in permission_classes for the view/viewset
"""

from functools import wraps

from rest_framework.permissions import IsAuthenticated

from knoxth.auth import IsScoped
from knoxth.models import Context


def withContext(_class=None, context=None):
    """
    withContext decorator is used to inject all the authorization code necessary
    to use Knox Tokens.

    There are two ways to use this decorator:
    1. With default context
    @withContext
    class SomeViewSet(viewsets.ModelViewSet):
        ...

    2. With custom context
    @withContext(context="some-context")
    class SomeViewSet(viewsets.ModelViewSet):
        ...

    Args:
      context: Default value = None

    Returns:
      wrapper for viewsets
    """

    def __with_context(Cls):
        """ """
        assert callable(Cls) or Cls is None

        @wraps(Cls, updated=())
        class __decorated(Cls):
            """wrapper class for"""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                SWSIsScoped = IsScoped

                if context:
                    _context_name = context
                else:
                    _context_name = Cls.__name__.replace("ViewSet", "").lower()
                SWSIsScoped.context = _context_name
                if IsAuthenticated not in self.permission_classes:
                    self.permission_classes.append(IsAuthenticated)
                self.permission_classes.append(SWSIsScoped)
                Context.objects.get_or_create(name=_context_name)

        return __decorated

    return __with_context(_class) if callable(_class) else __with_context
