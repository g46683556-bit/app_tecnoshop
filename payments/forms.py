from django import forms
from .models import PaymentMethod

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ["payment_type", "alias", "card_number", "card_expiry", "card_cvv"]
        widgets = {
            "payment_type": forms.Select(attrs={"class": "form-select"}),
            "alias": forms.TextInput(attrs={"class": "form-control"}),
            "card_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de tarjeta"}),
            "card_expiry": forms.TextInput(attrs={"class": "form-control", "placeholder": "MM/YY"}),
            "card_cvv": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "CVV"}),
        }
