from django.test import TestCase, Client
from django.contrib.auth.models import User
from unittest.mock import patch
from django.urls import reverse
from products.models import Product, Category
from cart.models import CartItem
from orders.models import Order

class TestOrderPayment(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

        self.category = Category.objects.create(name="Footwear")

        self.product = Product.objects.create(
            name="Casual Shoe",
            price=1000,
            category=self.category
        )

        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

        # Add address into session
        session = self.client.session
        session["order_address"] = {
            "full_name": "Test User",
            "phone": "9999999999",
            "address_line": "Test Street",
            "city": "Mumbai",
            "pincode": "400001",
        }
        session.save()

    @patch("orders.views.stripe.checkout.Session.create")
    def test_start_payment(self, mock_stripe):
        mock_stripe.return_value.url = "http://fake-stripe-url.com"

        url = reverse("start_payment")   # ✅ FIX HERE
        response = self.client.get(url)  # was wrong before

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("http://fake-stripe-url.com"))

    @patch("orders.views.stripe.checkout.Session.retrieve")
    def test_payment_success(self, mock_retrieve):
        mock_retrieve.return_value.payment_intent = "pi_test_123"

        response = self.client.get(
            reverse("payment_success") + "?session_id=fake_session"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_success.html")

        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.payment_id, "pi_test_123")
        self.assertEqual(order.total_amount, 2000)
