from django.db import IntegrityError
from django.test import TestCase

from knoxth import constants
from knoxth.models import Context, Scope


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


class ScopeTestCase(TestCase):
    def setUp(self):
        self.context = Context.objects.create(name="Hello")
        self.scope = Scope.objects.create(context=self.context,
                                          permissions=constants.ACCESS)

    def test_scope_with_no_context(self):
        with self.assertRaises(IntegrityError):
            Scope.objects.create(permissions=constants.ACCESS)

    def test_scope_with_no_perrmissions(self):
        with self.assertRaises(IntegrityError):
            Scope.objects.create()

    def test_add_unknown_perm_to_scope(self):
        self.scope.add_perm(78)       # throw  error
        self.assertEqual(self.scope.permissions,
                         constants.ACCESS)

    def test_add_known_perm_to_scope(self):
        self.scope.add_perm(constants.MODIFY)       # throw  error
        self.assertEqual(self.scope.permissions,
                         constants.ACCESS | constants.MODIFY)

    def test_del_known_perm_from_scope(self):
        self.scope.del_perm(constants.ACCESS)
        self.assertEqual(self.scope.permissions, 0)

    def test_del_unset_perm_from_scope(self):
        self.scope.del_perm(constants.MODIFY)
        self.assertEqual(self.scope.permissions, constants.ACCESS)
