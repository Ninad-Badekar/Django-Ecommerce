from django.contrib import admin
from .models import Product, Category, ProductSize

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductSize)
