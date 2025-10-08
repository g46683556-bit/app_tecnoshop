from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order  # 👈 importa tu modelo

@login_required
def profile(request):
    # Traer todos los pedidos del usuario logueado
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "account/profile.html", {
        "user": request.user,
        "orders": orders,   # 👈 pasamos pedidos al template
    })
