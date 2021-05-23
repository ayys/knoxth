from django.db import IntegrityError
from django.test import TestCase
from knoxth import constants
from knoxth.models import Context, Scope


class ScopeTestCase(TestCase):
    def setUp(self):
        self.context = Context.objects.create(name="Hello")
        self.scope = Scope.objects.create(context=self.context, permissions=constants.ACCESS)

    def test_scope_with_no_context(self):
        with self.assertRaises(IntegrityError):
            Scope.objects.create(permissions=constants.ACCESS)

    def test_scope_with_no_perrmissions(self):
        with self.assertRaises(IntegrityError):
            Scope.objects.create()

    def test_add_unknown_perm_to_scope(self):
        self.scope.add_perm(78)  # throw  error
        self.assertEqual(self.scope.permissions, constants.ACCESS)

    def test_get_permissions_set(self):
        self.assertEqual(self.scope.permissions_set, ["access"])

    def test_set_permissions_set(self):
        perms_set = ["access", "modify"]
        self.scope.permissions_set = perms_set
        self.assertEqual(self.scope.permissions_set, perms_set)
        self.assertEqual(self.scope.permissions, Scope.permissions_set_to_int(perms_set))

    def test_permissions_set_to_int(self):
        self.assertEqual(Scope.permissions_set_to_int(["access"]), constants.ACCESS)
        self.assertEqual(Scope.permissions_set_to_int(["modify"]), constants.MODIFY)
        self.assertEqual(Scope.permissions_set_to_int(["delete"]), constants.DELETE)
        self.assertEqual(Scope.permissions_set_to_int(["delete", "access"]), constants.DELETE | constants.ACCESS)

    def test_add_known_perm_to_scope(self):
        self.scope.add_perm(constants.MODIFY)  # throw  error
        self.assertEqual(self.scope.permissions, constants.ACCESS | constants.MODIFY)

    def test_del_known_perm_from_scope(self):
        self.scope.del_perm(constants.ACCESS)
        self.assertEqual(self.scope.permissions, 0)

    def test_del_unset_perm_from_scope(self):
        self.scope.del_perm(constants.MODIFY)
        self.assertEqual(self.scope.permissions, constants.ACCESS)
