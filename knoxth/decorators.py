import inspect
from functools import wraps

from knoxth.auth import IsScoped
from knoxth.models import Context


def withContext(_class=None, context=None):
    def _withContext(cls):
        assert callable(_class) or _class is None
        @wraps(cls, updated=())
        class _Decorated(cls):
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
        return _Decorated
    return _withContext(_class) if callable(_class)else _withContext
