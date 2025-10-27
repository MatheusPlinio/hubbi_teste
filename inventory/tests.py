from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from inventory.models import Part, ImportTask

User = get_user_model()


class PartAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="user123"
        )
        self.part = Part.objects.create(
            name="Parafuso", description="Parafuso de aço", price=1.50, quantity=100, category="Ferramentas"
        )

    def test_list_parts_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("part-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_part_admin_only(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("part-create")
        data = {
            "name": "Porca",
            "description": "Porca de aço",
            "price": 0.50,
            "quantity": 200,
            "category": "Ferramentas"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_part_admin_only(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("part-update", kwargs={"pk": self.part.id})
        response = self.client.patch(url, {"quantity": 500})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(url, {"quantity": 500})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.part.refresh_from_db()
        self.assertEqual(self.part.quantity, 500)

    def test_delete_part_admin_only(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("part-delete", kwargs={"pk": self.part.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ImportCSVTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )

    @patch("inventory.views.import_csv_task.delay")
    def test_import_csv_creates_task_and_triggers_celery(self, mock_task):
        self.client.force_authenticate(user=self.admin)
        url = reverse("import-csv")
        data = {"file_path": "/tmp/test.csv"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = ImportTask.objects.first()
        self.assertIsNotNone(task)
        mock_task.assert_called_once_with(task.id)

    def test_import_csv_requires_admin(self):
        user = User.objects.create_user(
            username="user", email="user@example.com", password="user123"
        )
        self.client.force_authenticate(user=user)
        url = reverse("import-csv")
        response = self.client.post(url, {"file_path": "/tmp/test.csv"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
