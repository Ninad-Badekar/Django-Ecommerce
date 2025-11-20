from django.http import HttpResponse
import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from cart.models import CartItem
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def start_payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect("/cart/")

    line_items = []
    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "inr",
                "unit_amount": int(item.product.price * 100),
                "product_data": {"name": item.product.name},
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://127.0.0.1:8000/orders/payment-success/?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/cart/",
    )

    return redirect(session.url)


def payment_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return HttpResponse("Missing session_id", status=400)

    # Retrieve the Stripe checkout session
    session = stripe.checkout.Session.retrieve(session_id)

    # Extract the real Stripe payment intent
    payment_intent_id = session.payment_intent

    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect("/")

    total = sum(item.product.price * item.quantity for item in cart_items)

    address = request.session.get("order_address")
    if not address:
        return HttpResponse("Missing address", status=400)

    # Create Order in database
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status="Paid",
        payment_id=payment_intent_id,   # Stripe official ID
        full_name=address["full_name"],
        phone=address["phone"],
        address_line=address["address_line"],
        city=address["city"],
        pincode=address["pincode"]
    )

    # Save order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return render(request, "orders/order_success.html", {"order": order})


def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


def enter_address(request):
    if request.method == "POST":
        request.session["order_address"] = {
            "full_name": request.POST["full_name"],
            "phone": request.POST["phone"],
            "address_line": request.POST["address_line"],
            "city": request.POST["city"],
            "pincode": request.POST["pincode"],
        }
        return redirect("start_payment")

    return render(request, "orders/address_form.html")
