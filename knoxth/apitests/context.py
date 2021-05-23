"""
Tests for contextual access to resource
In this test case, we test the view createdd in test_app app.
Refer to knoxth_project/urls.py and test_app/views.py for more info.
"""
from django.contrib.auth import get_user_model
from knox.models import AuthToken
from rest_framework.test import APIRequestFactory, APITestCase

from knoxth.views import AuthTokenViewset

User = get_user_model()


class ContextualAccessTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.username = "john.doe"
        self.email = "john.doe@example.com"
        self.password = "hunter2"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_contextual_access_without_proper_claim(self):
        (_, token) = AuthToken.objects.create(user=self.user)
        response = self.client.get("/users/", format="json", HTTP_AUTHORIZATION=("Token %s" % token))
        self.assertEqual(response.status_code, 403)

    def test_contextual_access_with_proper_claim(self):
        authobj, token = AuthToken.objects.create(user=self.user)
        authobj.claim.add_scope("users", permissions_set=["access"])
        response = self.client.get("/users/", HTTP_AUTHORIZATION=("Token %s" % token))
        self.assertEqual(response.status_code, 200)

    def test_contains_create_attr(self):
        self.assertTrue(hasattr(AuthTokenViewset(), "create"))
