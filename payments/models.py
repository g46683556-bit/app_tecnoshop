from django.db import models
from django.contrib.auth.models import User

class PaymentMethod(models.Model):
    PAYMENT_TYPES = [
        ("card", "Tarjeta de crédito/débito"),
        ("yape", "Yape / Plin"),
        ("cash", "Pago contra entrega"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    card_number = models.CharField(max_length=16, blank=True, null=True)   # Se enmascara
    card_expiry = models.CharField(max_length=5, blank=True, null=True)    # MM/YY
    card_cvv = models.CharField(max_length=4, blank=True, null=True)       # ⚠ Nunca guardar en producción real
    alias = models.CharField(max_length=50, blank=True, null=True)         # Ejemplo: "Visa Personal"

    created_at = models.DateTimeField(auto_now_add=True)

    def masked_card(self):
        """Retorna solo los últimos 4 dígitos para mostrar"""
        if self.card_number:
            return f"**** **** **** {self.card_number[-4:]}"
        return None

    def __str__(self):
        return f"{self.get_payment_type_display()} - {self.alias or self.masked_card()}"
