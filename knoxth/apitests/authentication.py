"""
Test the authentication process for knoxth

The process is as follows

1. Get the authorization token
2. Use authorization token to get access token
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase as TestCase

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        self.username = "john.doe"
        self.email = "john.doe@example.com"
        self.password = "hunter2"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.username2 = "jane.doe"
        self.email2 = "jane.doe@example.com"
        self.password2 = "hunter2"
        self.user2 = User.objects.create_user(self.username2, self.email2, self.password2)

    def test_get_authorization_code(self):
        url = reverse("knoxth:authorize")
        response = self.client.post(url, {"username": "john.doe", "password": "hunter2"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token1 = response.data.get("token")

        response = self.client.post(url, {"username": "jane.doe", "password": "hunter2"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token2 = response.data.get("token")

        self.assertNotEqual(token1, token2)

        return response.data.get("token")

    def test_get_access_token_with_authorization_code(self):
        token = self.test_get_authorization_code()
        url = reverse("knoxth:login")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        self.assertIn("expiry", response.data)
        return (token, response.data.get("token"))

    def test_cannot_use_same_authorization_code_after_logout(self):
        auth_code, token = self.test_get_access_token_with_authorization_code()
        url = reverse("knoxth:logout")
        login_url = reverse("knoxth:login")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 204)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + auth_code)
        response = self.client.post(login_url, format="json")
        self.assertEqual(response.status_code, 401)
