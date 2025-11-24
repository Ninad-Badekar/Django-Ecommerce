from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CartItem
from products.models import Product


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            item.quantity += 1
            item.save()

        return redirect("cart")


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.delete()
        return redirect("cart")


class IncreaseQuantityView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.quantity += 1
        item.save()
        return redirect("cart")


class DecreaseQuantityView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, user=request.user)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

        return redirect("cart")


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, "cart/cart.html", {"cart_items": cart_items})
