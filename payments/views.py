from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PaymentMethod
from .forms import PaymentMethodForm

@login_required
def payment_methods(request):
    """Lista todos los métodos de pago del usuario"""
    methods = request.user.payment_methods.all()
    return render(request, "pages/payment_methods.html", {"methods": methods})


@login_required
def add_payment_method(request):
    """Agregar un nuevo método de pago"""
    if request.method == "POST":
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            return redirect("payments:payment_methods")
    else:
        form = PaymentMethodForm()
    return render(request, "pages/add_payment_method.html", {"form": form})


@login_required
def delete_payment_method(request, pk):
    """Eliminar un método de pago"""
    method = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    if request.method == "POST":
        method.delete()
        return redirect("payments:payment_methods")
    return render(request, "pages/confirm_delete.html", {"method": method})
