from django.contrib import admin
from .models import Order, OrderItem   # whatever your model names are

admin.site.register(Order)
admin.site.register(OrderItem)
