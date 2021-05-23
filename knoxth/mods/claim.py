"""
Claim Model for knoxth.

from knoxth.models import Claim
"""
from django.db import models
from knox.models import AuthToken as KnoxToken

from knoxth.constants import ACCESS, DELETE, MODIFY
from knoxth.mods.context import Context
from knoxth.mods.scope import Scope


# Create your models here.
class Claim(models.Model):
    """
    A claim holds information about scopes associated with
    a specific token
    """

    name = models.CharField(max_length=255)
    token = models.OneToOneField(KnoxToken, on_delete=models.CASCADE)
    scopes = models.ManyToManyField(Scope)

    def add_scope(self, context: str, permissions: int = None, permissions_set: list = None):
        """
        Adds a scope with given context and permissions

        The permissions need to be bitwise-ORed as such:
        ACCESS | MODIFY | DELETE

        context has to be a string.
        """

        if permissions_set is not None:
            permissions = Scope.permissions_set_to_int(permissions_set)

        return self.scopes.get_or_create(
            context=Context.objects.get_or_create(name=context)[0],
            permissions=permissions,
        )[0]

    def del_scope(self, context: str, permissions: int = ACCESS | MODIFY | DELETE):
        """
        Delete a scope with the given context and permissions. If scopes don't match, do nothing.
        """
        return self.scopes.filter(context__name=context, permissions=permissions).delete()

    def del_scopes_with_context(self, context: str):
        """
        Delete all scopes with the given context.
        """
        return self.scopes.filter(context__name=context).delete()

    def verify(self, context: str, permission: int) -> bool:
        """
        Verifies that the claim accepts given permissions for the given context.
        """
        return len([1 for _ in self.scopes.filter(context__name=context) if _.permissions & permission != 0]) > 0

    def __str__(self):
        return f"Token {self.token.digest[:5]}... has {[_ for _ in self.scopes.all()]} scopes"
