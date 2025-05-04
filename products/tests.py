from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product, Category


class BookAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        self.admin_user = User.objects.create_user(
            username="admin_user", password="password", is_staff=True
        )
        self.category = Category.objects.create(name="Test Category")

        self.product_data = {
            "name": "Test Product",
            "price": 12,
            "description": "Test Description",
            "category": [self.category.id],
            "available": True,
        }

        self.product = Product.objects.create(
            name="Test Product",
            price=12,
            description="Test Description",
            available=True,
        )
        self.product.category.add(self.category)

        self.product_create_url = reverse("products:product_create")
        self.product_list_url = reverse("products:product_list")
        self.product_detail_url = reverse("products:product_detail", args=[self.product.id])
        self.product_update_url = reverse("products:product_detail", args=[self.product.id])

    def test_create_product_as_admin(self):
        self.client.login(username="admin_user", password="password")
        response = self.client.post(self.product_create_url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.product_data["name"])

    def test_create_product_as_normal_user(self):
        self.client.login(username="test_user", password="password")
        response = self.client.post(self.product_create_url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_product_list(self):
        self.client.login(username="test_user", password="password")
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        self.client.login(username="test_user", password="password")
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_delete_product_as_admin(self):
        self.client.login(username="admin_user", password="password")
        response = self.client.delete(self.product_update_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_delete_product_as_normal_user(self):
        self.client.login(username="test_user", password="password")
        response = self.client.delete(self.product_update_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_product_by_category(self):
        self.client.login(username="test_user", password="password")
        url = reverse("products:products_category", args=[self.category.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.product.name)
