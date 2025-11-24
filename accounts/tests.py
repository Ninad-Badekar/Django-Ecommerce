from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.home_url = reverse("home")


    def test_register_user_success(self):
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "email": "newuser@test.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123"
        })

        if response.status_code == 200:
            print("Form errors:", response.context["form"].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username="newuser").exists())


    def test_register_password_mismatch(self):
        response = self.client.post(self.register_url, {
            "username": "baduser",
            "email": "bad@test.com",
            "password1": "Testpass123",
            "password2": "Wrongpass123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="baduser").exists())


    def test_login_success(self):
        User.objects.create_user(username="testuser", password="testpass123")

        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

  
    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            "username": "wrong",
            "password": "wrong"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")


    def test_logout(self):
        user = User.objects.create_user(username="logoutuser", password="test123456")
        self.client.login(username="logoutuser", password="test123456")

        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
