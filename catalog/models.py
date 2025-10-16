import uuid
from decimal import Decimal
from django.db import models

class Catalog(models.Model):
    CATEGORIES = [
        ("celulares", "Celulares"),
        ("tablets", "Tablets"),
        ("laptops", "Laptops"),
        ("dispositivos-personales", "Dispositivos personales"),
        ("computadoras", "Computadoras"),
        ("audio", "Audio"),
        ("imagen-video", "Imagen y video"),
        ("hogar-inteligente", "Hogar inteligente"),
        ("gaming", "Gaming"),
        ("accesorios", "Accesorios"),
    ]

    name = models.CharField(
        max_length=200,
        help_text="Nombre de producto",
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=64,
        help_text="Identificador único tipo hash (64 caracteres) para la URL del producto",
    )
    description = models.TextField(
        blank=True,
        help_text="Descripción detallada del producto",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio en formato decimal (ejemplo: 1200.50)",
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en inventario",
    )
    image_url = models.URLField(
        max_length=700,
        blank=True,
        help_text="Link directo a la imagen del producto",
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORIES,
        help_text="Selecciona la categoría del producto",
    )

    def __str__(self):
        return f"{self.name} - {self.category}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generar un hash único de 64 caracteres usando uuid4.hex repetido
            hash_full = (uuid.uuid4().hex + uuid.uuid4().hex)[:64]
            self.slug = hash_full
        super().save(*args, **kwargs)



    # 🟢 Nuevo: descuento en porcentaje (ej. 15 para 15%)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Descuento en porcentaje (ejemplo: 15 para 15%)",
    )

    # 🟢 Nuevo: campo opcional para un precio con descuento fijo
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Precio con descuento (si aplica)",
    )

    def __str__(self):
        return f"{self.name} - {self.category}"

    @property
    def final_price(self):
        """Devuelve el precio final considerando descuentos."""
        if self.discount_price:
            return self.discount_price
        if self.discount_percent > 0:
            descuento = self.price * (self.discount_percent / Decimal(100))
            return round(self.price - descuento, 2)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            hash_full = (uuid.uuid4().hex + uuid.uuid4().hex)[:64]
            self.slug = hash_full
        super().save(*args, **kwargs)
