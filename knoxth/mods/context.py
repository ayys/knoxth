"""
The Context Model

from knoxth.models import Context
"""

from django.db import models


class Context(models.Model):
    """
    Context model currently only has a name.
    A context is a view or viewset, for which a scope
    stores the permissions. Contexts are used to separately
    manage permissions for each viewset.
    """

    name = models.CharField(default=None, max_length=64, unique=True)

    def __str__(self):
        return self.name
