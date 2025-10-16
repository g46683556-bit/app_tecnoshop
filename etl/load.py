import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_tecnoshop.settings")
django.setup()

from django.conf import settings
from catalog.models import Catalog



def load_to_db(df):
    print("📁 Base de datos activa:", settings.DATABASES['default']['NAME'])
    print(df.head(10).to_string())


    for _, row in df.iterrows():
        product, created = Catalog.objects.update_or_create(
            name=row["name"],
            defaults={
                "description": row["description"],
                "price": row["price"],
                "discount_percent": row["discount_percent"],
                "discount_price": row["discount_price"],
                "stock": int(row["stock"]) if str(row["stock"]).isdigit() else 0,
                "image_url": row["image_url"],
                "category": row["category"],
            },
        )
        print(f"{'🆕 Creado' if created else '🔁 Actualizado'}: {product.name}")
