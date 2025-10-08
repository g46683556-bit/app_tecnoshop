from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.models import Catalog
from .models import Cart, CartItem

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "pages/cart.html", {"cart": cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Catalog, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Si el producto ya está en el carrito, aumentar cantidad
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()  # Si ponen 0, eliminamos
    return redirect("cart")

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        item.delete()
    return redirect("cart")
