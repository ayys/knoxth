"""
Scope Model for knoxth

from knoxth.models import Scope
"""
import functools

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

    context = models.ForeignKey(Context, on_delete=models.CASCADE)

    permissions = models.IntegerField(
        choices=[("ACCESS", ACCESS), ("MODIFY", MODIFY), ("DELETE", DELETE)],
        default=ALL_PERMISSIONS,
    )

    @staticmethod
    def permissions_set_to_int(perms):
        """
        Convert the permission strings to integer
        """
        perm_ints = map(
            lambda perm: ACCESS if perm.lower() == "access" else MODIFY if perm.lower() == "modify" else DELETE if perm.lower() == "delete" else 0,
            perms,
        )
        return functools.reduce(lambda p1, p2: p1 | p2, perm_ints)

    @property
    def permissions_set(self):
        permissions = [
            "access" if self.permissions & ACCESS else None,
            "modify" if self.permissions & MODIFY else None,
            "delete" if self.permissions & DELETE else None,
        ]
        return [_ for _ in permissions if _ is not None]

    @permissions_set.setter
    def permissions_set(self, new_perms_set):
        self.permissions = Scope.permissions_set_to_int(new_perms_set)

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
        return f"""{", ".join(self.permissions_set)} permissions for "{self.context.name}" context"""
