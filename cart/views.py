from django.shortcuts import redirect, render, get_object_or_404
from .models import CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        item.quantity += 1
        item.save()
    
    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect("cart")


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect("cart")


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()   # auto remove when qty = 0

    return redirect("cart")


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, "cart/cart.html", {"cart_items": cart_items})
