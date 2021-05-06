from django.db import models
from knoxth.constants import ACCESS, ALL_PERMISSIONS, DELETE, MODIFY
from knoxth.mod.context import Context


class Scope(models.Model):
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE)

    permissions = models.IntegerField(
        choices=[("ACCESS", ACCESS),
                 ("MODIFY", MODIFY),
                 ("DELETE", DELETE)],
        default=ALL_PERMISSIONS)

    def add_perm(self, perm):
        if perm in [ACCESS, MODIFY, DELETE]:
            self.permissions = self.permissions | perm
            self.save()
        return self.permissions


    def del_perm(self, perm):
        if perm in [ACCESS, MODIFY, DELETE]:
            self.permissions = self.permissions & ~perm
            self.save()
        return self.permissions

    def __str__(self):
        return f"Permissions for {self.context.name}"
