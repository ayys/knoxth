'''
Implementation of `withContext` decorator.

from knoxth.decorators import withContext

This decorator does two things:
1. Injects a class property `context` to isScoped with the value equal to current context
2. Injects IsScoped in permission_classes for the view/viewset
'''

import inspect
from functools import wraps

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
    @withContext("some-context")
    class SomeViewSet(viewsets.ModelViewSet):
        ...

    Args:
      context: Default value = None)

    Returns:
      wrapper for viewsets
    """
    def __withContext(cls):
        """ """
        assert callable(_class) or _class is None
        @wraps(cls, updated=())
        class __Decorated(cls):
            """ """
            def __init__(self, *args, **kwargs):
                super(cls, self).__init__(*args, **kwargs)
                SWSIsScoped = IsScoped

                if context:
                    _context_name = context
                else:
                    _context_name = cls.__name__\
                                       .replace("ViewSet", "")\
                                       .lower()
                SWSIsScoped.context = _context_name
                self.permission_classes.append(SWSIsScoped)
                Context.objects.get_or_create(name=_context_name)
        return __Decorated
    return __withContext(_class) if callable(_class)else _withContext
