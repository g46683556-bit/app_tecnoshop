from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("", views.payment_methods, name="payment_methods"),
    path("add/", views.add_payment_method, name="add_method"),
    path("delete/<int:pk>/", views.delete_payment_method, name="delete_method"),
]
