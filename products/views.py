from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, ProductSize

def home_view(request):

    products = Product.objects.all()
    categories = Category.objects.all()
    sizes = ProductSize.objects.values_list("size", flat=True).distinct()

    # GET Filters
    search = request.GET.get("search")
    category = request.GET.get("category")
    brand = request.GET.get("brand")
    size = request.GET.get("size")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    # Search
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(brand__icontains=search)
        )

    # Category
    if category:
        products = products.filter(category_id=category)

    # Brand
    if brand:
        products = products.filter(brand__icontains=brand)

    # Price filters
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Size
    if size:
        products = products.filter(sizes__size=size, sizes__quantity__gt=0).distinct()

    # Sorting
    if sort == "price_low":
        products = products.order_by("price")
    elif sort == "price_high":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-id")

    return render(request, "products/home.html", {
        "products": products,
        "categories": categories,
        "sizes": sizes,
        "request": request,   # needed for maintaining selected filters
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})
