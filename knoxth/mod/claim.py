from django.db import models
from knox.models import AuthToken as KnoxToken
from knoxth.constants import ACCESS, DELETE, MODIFY
from knoxth.mod.context import Context
from knoxth.mod.scope import Scope


# Create your models here.
class Claim(models.Model):
    '''
    A claim holds information about scopes associated with
    a specific token
    '''
    token = models.OneToOneField(KnoxToken, on_delete=models.CASCADE)
    scopes = models.ManyToManyField(Scope)

    def add_scope(self, context, permissions):
        return self.scopes.get_or_create(
            context=Context.objects.get_or_create(name=context)[0],
            permissions=permissions)[0]

    def del_scope(self, context, permissions=ACCESS|MODIFY|DELETE):
        return self.scopes.filter(
            context__name=context,
            permissions=permissions).delete()

    def del_scope_with_context(self, context):
        return self.scopes.filter(context__name=context).delete()

    def verify(self, context, permission):
        return len(
            [
                1
                for _ in self.scopes.filter(context__name=context)
                if _.permissions & permission != 0
             ]) > 0

    def __str__(self):
        return f"Token {self.token.digest[:5]}... has {[_ for _ in self.scopes.all()]} scopes"
