from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category

def get_test_image():
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\x47\x49\x46\x38\x39\x61', 
        content_type='image/jpeg'
    )


class ProductViewsTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Shoes")

        self.product1 = Product.objects.create(
            name="Running Shoe",
            price=1999,
            category=self.category,
            brand="Nike",
            image=get_test_image()   # ✅ Added image
        )

        self.product2 = Product.objects.create(
            name="Casual Shoe",
            price=1499,
            category=self.category,
            brand="Puma",
            image=get_test_image()   
        )

    def test_product_list_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Running Shoe")
        self.assertContains(response, "Casual Shoe")

    def test_product_detail_page(self):
        response = self.client.get(reverse("product_detail", args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Running Shoe")
        self.assertContains(response, "1999")

    def test_product_creation(self):
        product = Product.objects.get(name="Running Shoe")
        self.assertEqual(product.price, 1999)
        self.assertTrue(product.image)  

    def test_category_exists(self):
        self.assertEqual(self.category.name, "Shoes")
