import pandas as pd
from decimal import Decimal

# Mapeo de categorías externas → internas
CATEGORY_MAP = {
    "accesorios": "accesorios",
    "accesorioss": "accesorios",
    "gaming": "gaming",
    "imagen y vídeo": "imagen-video",
    "imagen y video": "imagen-video",
    "imagen-video": "imagen-video",
    "tablets": "tablets",
    "computadoras": "computadoras",
}

def clean_price(value):
    """Convierte valores tipo 'S/399', '1.999,90', '499.50' a Decimal limpio."""
    if pd.isna(value):
        return Decimal("0")
    text = str(value).lower()
    text = text.strip().replace('"', '').replace("'", "")
    text = text.replace("s/", "").replace("soles", "")
    text = text.replace(" ", "").replace(",", "")
    try:
        return Decimal(text)
    except:
        return Decimal("0")

def clean_discount(value):
    """Convierte '15%' o '15,00' a número decimal."""
    if pd.isna(value):
        return Decimal("0")
    text = str(value).replace("%", "").replace(",", ".").replace('"', '').strip()
    try:
        return Decimal(text)
    except:
        return Decimal("0")

def normalize_category(cat):
    """Normaliza y mapea categorías."""
    if not cat:
        return "accesorios"
    cat = str(cat).strip().lower().replace('"', "")
    return CATEGORY_MAP.get(cat, "accesorios")

def normalize_url(url):
    """Asegura HTTPS y elimina espacios y comillas."""
    if not isinstance(url, str):
        return ""
    url = url.strip().replace('"', '')
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    return url

def transform_data(df):
    """Transforma y limpia el DataFrame del CSV para ser cargado a Catalog."""
    # Normalizar encabezados
    df.columns = [c.strip().lower() for c in df.columns]

    # Renombrar columnas
    df = df.rename(columns={
        "nombre": "name",
        "descripcion": "description",
        "precio": "price",
        "stock": "stock",
        "categoria": "category",
        "imagen": "image_url",
        "descuento_porcentaje": "discount_percent",
    })

    # Limpiar valores
    df["name"] = df["name"].astype(str).str.strip().str.replace('"', '')
    df["description"] = df["description"].astype(str).str.strip().str.replace('"', '')
    df["price"] = df["price"].apply(clean_price)
    df["discount_percent"] = df["discount_percent"].apply(clean_discount)
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)
    df["category"] = df["category"].apply(normalize_category)
    df["image_url"] = df["image_url"].apply(normalize_url)

    # Calcular descuento final
    df["discount_price"] = df["price"] * (1 - df["discount_percent"] / 100)

    # Rellenar columnas faltantes
    df["slug"] = None

    print("✅ Datos transformados correctamente.")
    print(df.head(5))  # Mostrar vista previa
    return df
