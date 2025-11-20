from .models import Product
from django.shortcuts import render,get_object_or_404

def home_view(request):
    products = Product.objects.all()
    return render(request, "products/home.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})
