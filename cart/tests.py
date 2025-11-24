from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from products.models import Product, Category
from cart.models import CartItem


class CartViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Create user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # Login user
        self.client.login(username="testuser", password="testpass123")

        # Create category & product
        self.category = Category.objects.create(name="Footwear")

        self.product = Product.objects.create(
            name="Running Shoe",
            price=1200,
            category=self.category
        )

        # Create initial cart item
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def test_add_to_cart_view(self):
        CartItem.objects.all().delete()   # clear existing item for test

        response = self.client.get(
            reverse("add_to_cart", args=[self.product.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 1)

        item = CartItem.objects.first()
        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.product, self.product)

    def test_add_to_cart_increases_quantity(self):
        response = self.client.get(
            reverse("add_to_cart", args=[self.product.id])
        )

        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 2)

    def test_remove_from_cart(self):
        response = self.client.get(
            reverse("remove_from_cart", args=[self.cart_item.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_increase_quantity(self):
        response = self.client.get(
            reverse("increase_quantity", args=[self.cart_item.id])
        )

        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 2)

    def test_decrease_quantity(self):
        self.cart_item.quantity = 2
        self.cart_item.save()

        response = self.client.get(
            reverse("decrease_quantity", args=[self.cart_item.id])
        )

        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 1)

    def test_decrease_quantity_removes_item(self):
        # When quantity is 1 → item should be deleted
        response = self.client.get(
            reverse("decrease_quantity", args=[self.cart_item.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_detail_view(self):
        response = self.client.get(reverse("cart"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")
        self.assertContains(response, self.product.name)
