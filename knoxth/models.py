"""
meta module for all the models in knoxth
"""

from django.db import models
from django.dispatch import receiver
from knox.models import AuthToken

from knoxth.mods.claim import Claim
from knoxth.mods.context import Context
from knoxth.mods.scope import Scope


@receiver(models.signals.post_save, sender=AuthToken)
def create_claim_for_authtoken(sender, instance, created, **kwargs):
    """
    Create a default claim for all tokens
    """
    if created:
        Claim.objects.create(name="Main", token=instance)


@receiver(models.signals.post_delete, sender=AuthToken)
def delete_claim_if_possible(sender, instance, **kwargs):
    """
    Create a default claim for all tokens
    """
    claims = Claim.objects.filter(token=instance)
    if not AuthToken.objects.filter(~models.Q(pk=instance.pk)).filter(claim__in=claims).exists():
        # if other auth tokens do not contain the claim belonging to this auth token,
        # delete the claims
        claims.delete()
