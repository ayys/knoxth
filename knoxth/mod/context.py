from django.db import models


# Create your models here.
class Context(models.Model):
    name = models.CharField(
        default=None,
        max_length=64,
        unique=True)

    def __str__(self):
        return self.name
