from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class UserLoginAPIViewTest(TestCase):
    def setUp(self):
        self.login_url = reverse('accounts:user_login')
        self.logout_url = reverse('accounts:user_logout')
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_login_successful(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Успешная авторизация')

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'nonexistenpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def authenticate(self):
        self.client.login(username='testuser', password='testpassword123')

    def test_post_logout_authenticated(self):
        self.authenticate()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Успешный выход')

    def test_post_logout_unauthenticated(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
