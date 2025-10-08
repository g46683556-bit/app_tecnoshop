from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", cart_view, name="cart"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", update_cart, name="update_cart"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
]
