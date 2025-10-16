from django.core.management.base import BaseCommand
from etl.extract import extract_from_csv
from etl.transform import transform_data
from etl.load import load_to_db

class Command(BaseCommand):
    help = "Ejecuta el pipeline ETL completo"

    def handle(self, *args, **options):
        print("🔹 Iniciando ETL...")

        # 1️⃣ EXTRAER
        df = extract_from_csv("data/data_impura.csv")
        print(f"✅ Archivo data/data_impura.csv cargado con {len(df)} filas válidas.")
        print(f"📥 {len(df)} registros leídos")

        # 🔹 Renombrar columnas a formato estándar (inglés)
        df = df.rename(columns={
            "nombre": "name",
            "descripcion": "description",
            "precio": "price",
            "categoria": "category",
            "imagen": "image_url",
            "descuento_porcentaje": "discount_percent",
        })
        print(f"🔄 Columnas después de renombrar: {list(df.columns)}")

        # 2️⃣ TRANSFORMAR
        df = transform_data(df)

        # 🔍 Debug opcional
        print(df.dtypes)
        print(df.head())

        # 3️⃣ CARGAR
        load_to_db(df)

        print("✅ ETL completado con éxito 🚀")
