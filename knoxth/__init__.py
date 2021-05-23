"""
knoxth implements an authorization layer on top of DRF and Knox by implementing
Scope based authorization for Knox Tokens.

To use knoxth, simply annotate your viewsets with @withContext decorator as such.

from knoxth.decorators import withContext

@withContext
class SomeViewSet(viewsets.ModelViewSet):
    ...
"""

__version__ = "0.0.1"
