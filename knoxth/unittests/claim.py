from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from knox.models import AuthToken as KnoxToken

from knoxth import constants
from knoxth.models import Claim, Context, Scope


class ClaimTestCase(TestCase):
    def setUp(self):
        self.context = Context.objects.create(name="Hello")

        self.scope = Scope.objects.create(context=self.context, permissions=constants.ACCESS)

        self.user = User.objects.create(username="ayush", email="meow@meow.com", password="meow")

        self.auth, self.token = KnoxToken.objects.create(user=self.user)
        self.auth.claim.delete()

    def test_claim_with_no_token_or_scopes(self):
        with self.assertRaises(IntegrityError):
            Claim.objects.create()

    def test_claim_with_no_scopes_no_names(self):
        Claim.objects.create(token=self.auth)

    def test_claim_add_scope_with_nonexistant_context(self):
        claim = Claim.objects.create(token=self.auth)
        prev_scope_count = claim.scopes.all().count()
        claim.add_scope("random-context", constants.ACCESS | constants.MODIFY)
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count + 1)

    def test_claim_add_scope_with_existing_context(self):
        claim = Claim.objects.create(token=self.auth)
        prev_scope_count = claim.scopes.all().count()
        claim.add_scope("Hello", constants.ACCESS | constants.MODIFY)
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count + 1)

    def test_claim_delete_all_scopes_with_existing_context(self):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        claim.add_scope("Second Context", constants.ACCESS | constants.MODIFY)
        prev_scope_count = claim.scopes.all().count()
        claim.del_scopes_with_context("Second Context")
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count - 1)

    def test_claim_delete_scopes_with_nonexistant_context(self):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        claim.add_scope("Second Context", constants.ACCESS | constants.MODIFY)
        prev_scope_count = claim.scopes.all().count()
        claim.del_scopes_with_context("Third Context")
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count)

    def test_claim_delete_scopes_with_existing_context_and_different_permissions(self):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        claim.add_scope("Second Context", constants.ACCESS | constants.MODIFY)
        prev_scope_count = claim.scopes.all().count()
        claim.del_scope("First Context")
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count)

    def test_claim_delete_scopes_with_existing_context_and_same_permissions(self):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        claim.add_scope("Second Context", constants.ACCESS | constants.MODIFY)
        prev_scope_count = claim.scopes.all().count()
        claim.del_scope("First Context", constants.ACCESS | constants.MODIFY)
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count - 1)

    def test_claim_delete_scopes_with_nonexistant_context_and_same_permissions(self):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        claim.add_scope("Second Context", constants.ACCESS | constants.MODIFY)
        prev_scope_count = claim.scopes.all().count()
        claim.del_scope("Third Context", constants.ACCESS | constants.MODIFY)
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count)

    def test_claim_delete_scopes_with_nonexistant_context_and_different_permissions(
        self,
    ):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        claim.add_scope("Second Context", constants.ACCESS | constants.MODIFY)
        prev_scope_count = claim.scopes.all().count()
        claim.del_scope("First Context")
        final_scope_count = claim.scopes.all().count()
        self.assertEqual(final_scope_count, prev_scope_count)

    def test_claim_verify_existing_context_and_permission(self):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        self.assertEqual(claim.verify("First Context", constants.MODIFY), True)
        self.assertEqual(claim.verify("First Context", constants.ACCESS), True)
        self.assertEqual(claim.verify("First Context", constants.DELETE), False)

    def test_claim_verify_nonexisting_context_and_permission(self):
        claim = Claim.objects.create(token=self.auth)
        claim.add_scope("First Context", constants.ACCESS | constants.MODIFY)
        self.assertEqual(claim.verify("Second Context", constants.MODIFY), False)
        self.assertEqual(claim.verify("Second Context", constants.ACCESS), False)
        self.assertEqual(claim.verify("Second Context", constants.DELETE), False)
