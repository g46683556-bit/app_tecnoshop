from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        if not cart.items.exists():
            return redirect("cart")  # Evita checkout vacío

        # Crear la orden
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total=cart.total(),
        )

        # Guardar los items del carrito en la orden
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Vaciar el carrito
        cart.items.all().delete()

        return redirect("order_success", order_id=order.id)

    return render(request, "pages/checkout.html", {"cart": cart})

def order_success(request, order_id):
    from .models import Order
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "pages/order_success.html", {"order": order})
