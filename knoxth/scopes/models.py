from constants import ACCESS, ALL_PERMISSIONS, DELETE, MODIFY
from django.db import models


# Create your models here.
class Context(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Scope(models.Model):
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE,
        null=True)

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