from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Order, OrderItem
from inventory.models import Part

User = get_user_model()


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_user",
            email="admin@example.com",
            password="password",
            is_staff=True
        )

        self.user = User.objects.create_user(
            username="normal_user",
            email="user@example.com",
            password="password",
            is_staff=False
        )

        self.part = Part.objects.create(
            name="Peça Teste",
            description="Descrição",
            price=100,
            quantity=50,
            category="Teste"
        )

        self.order = Order.objects.create(
            user=self.user,
            status="pending",
            total_price=100
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            piece=self.part,
            quantity=1,
            unit_price=100,
            subtotal=100
        )

    def login_and_get_token(self, email, password):
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {"email": email, "password": password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access"]

    def auth_client(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_order_list_authenticated(self):
        token = self.login_and_get_token("user@example.com", "password")
        self.auth_client(token)
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_create(self):
        token = self.login_and_get_token("user@example.com", "password")
        self.auth_client(token)
        url = reverse("order-create")
        data = {"status": "pending"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.last().user, self.user)

    def test_order_retrieve(self):
        token = self.login_and_get_token("user@example.com", "password")
        self.auth_client(token)
        url = reverse("order-detail", kwargs={"pk": self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order.id)

    def test_order_update_admin_only(self):
        token = self.login_and_get_token("user@example.com", "password")
        self.auth_client(token)
        url = reverse("order-detail", kwargs={"pk": self.order.id})
        data = {"status": "paid"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.login_and_get_token("admin@example.com", "password")
        self.auth_client(token)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "paid")

    def test_order_delete_admin_only(self):
        token = self.login_and_get_token("user@example.com", "password")
        self.auth_client(token)
        url = reverse("order-detail", kwargs={"pk": self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.login_and_get_token("admin@example.com", "password")
        self.auth_client(token)
        url = reverse("order-detail", kwargs={"pk": self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_orderitem_create(self):
        token = self.login_and_get_token("user@example.com", "password")
        self.auth_client(token)
        url = reverse("orderitem-create")
        data = {
            "order_id": self.order.id,
            "piece_id": self.part.id,
            "quantity": 2,
            "unit_price": 50
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_orderitem_delete(self):
        token = self.login_and_get_token("user@example.com", "password")
        self.auth_client(token)
        url = reverse("orderitem-delete", kwargs={"pk": self.order_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(id=self.order_item.id).exists())
