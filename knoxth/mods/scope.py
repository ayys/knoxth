"""
Scope Model for knoxth

from knoxth.models import Scope
"""

from django.db import models

from knoxth.constants import ACCESS, ALL_PERMISSIONS, DELETE, MODIFY
from knoxth.mods.context import Context


class Scope(models.Model):
    """
    A scope stores permissions for a specific context.
    Scope enables users to control the authorization
    for each context independently.

    It has two methods:

    add_perm(perm) -> adds a permission to this scope

    del_perm(perm) ->  deletes a permission from this scope

    """
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE)

    permissions = models.IntegerField(
        choices=[("ACCESS", ACCESS),
                 ("MODIFY", MODIFY),
                 ("DELETE", DELETE)],
        default=ALL_PERMISSIONS)

    def add_perm(self, perm: int) -> int:
        """
        Adds a permission to this scope and returns the current permissions.
        """
        if perm in [ACCESS, MODIFY, DELETE]:
            self.permissions = self.permissions | perm
            self.save()
        return self.permissions

    def del_perm(self, perm: int) -> int:
        """
        Deletes a permission from this scope and returns the current permissions.
        """
        if perm in [ACCESS, MODIFY, DELETE]:
            self.permissions = self.permissions & ~perm
            self.save()
        return self.permissions

    def __str__(self):
        return f"Permissions for {self.context.name}"
