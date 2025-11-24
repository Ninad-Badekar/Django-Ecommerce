from django.urls import path
from . import views

urlpatterns = [
    path("start-payment/", views.start_payment, name="start_payment"),   
    path("payment-success/", views.payment_success, name="payment_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("enter-address/", views.enter_address, name="enter_address"),
]
