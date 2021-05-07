import inspect
from functools import wraps

from knoxth.auth import IsScoped
from knoxth.models import Context


def withContext(context_name=None):
    def _withContext(cls):
        @wraps(cls, updated=())
        class _Decorated(cls):
            def __init__(self, *args, **kwargs):
                super(cls, self).__init__(*args, **kwargs)
                SWSIsScoped = IsScoped

                if context_name:
                    _context_name = context_name
                else:
                    _context_name = cls.__name__\
                                       .replace("ViewSet", "")\
                                       .lower()

                SWSIsScoped.context = _context_name
                self.permission_classes.append(SWSIsScoped)
                Context.objects.get_or_create(name=_context_name)
        return _Decorated
    return _withContext
