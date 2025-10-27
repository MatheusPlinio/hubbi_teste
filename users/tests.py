from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="Password123!"
        )

    def test_register_user(self):
        url = reverse("user_register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPass123!",
            "password2": "NewPass123!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_register_user_password_mismatch(self):
        url = reverse("user_register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPass123!",
            "password2": "WrongPass123!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def login_and_get_token(self, email, password):
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {"email": email, "password": password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        return response.data["access"]

    def test_login_user(self):
        token = self.login_and_get_token("user@example.com", "Password123!")
        self.assertIsNotNone(token)

    def test_get_user_detail_authenticated(self):
        token = self.login_and_get_token("user@example.com", "Password123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("user_detail")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "user@example.com")
        self.assertEqual(response.data["username"], "testuser")

    def test_change_password(self):
        token = self.login_and_get_token("user@example.com", "Password123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("change_password")
        data = {
            "old_password": "Password123!",
            "new_password": "NewPassword123!"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)

        # testar login com nova senha
        token_new = self.login_and_get_token("user@example.com", "NewPassword123!")
        self.assertIsNotNone(token_new)

    def test_change_password_wrong_old(self):
        token = self.login_and_get_token("user@example.com", "Password123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("change_password")
        data = {
            "old_password": "WrongPassword!",
            "new_password": "NewPassword123!"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data)
