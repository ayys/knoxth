from unittest import TestCase

from knoxth.decorators import withContext
from rest_framework.viewsets import ReadOnlyModelViewSet


class TestWithContextDecorator(TestCase):
    def test_decorator_without_parens(self):
        @withContext
        class TestViewSet(ReadOnlyModelViewSet):
            ...
