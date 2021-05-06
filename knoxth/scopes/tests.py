import constants
from django.db import IntegrityError
from django.test import TestCase

from scopes.models import Context, Scope


# Create your tests here.
class ContextTestCase(TestCase):
    def setUp(self):
        context_a = Context.objects.create(name="home")
        context_diff_from_a = Context.objects.create(name="Animal")

    def test_context_exists(self):
        count = Context.objects.all().count()
        self.assertEqual(count, 2)

    def test_context_name_is_None(self):
        with self.assertRaises(IntegrityError):
            Context.objects.create(name=None)

    def test_context_name_is_unspecified(self):
        with self.assertRaises(IntegrityError):
            Context.objects.create()

    def test_context_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Context.objects.create(name="home")
