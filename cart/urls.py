from django.urls import path
from .views import (
    AddToCartView,
    RemoveFromCartView,
    IncreaseQuantityView,
    DecreaseQuantityView,
    CartDetailView
)

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart"),
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("increase/<int:item_id>/", IncreaseQuantityView.as_view(), name="increase_quantity"),
    path("decrease/<int:item_id>/", DecreaseQuantityView.as_view(), name="decrease_quantity"),
]
