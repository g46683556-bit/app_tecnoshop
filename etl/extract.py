import pandas as pd

def extract_from_csv(path):
    """Lee datos del CSV y los devuelve como DataFrame limpio."""
    try:
        # Leer CSV con autodetección de delimitador
        df = pd.read_csv(path, sep=None, engine="python", quotechar='"')
        print(f"✅ Archivo {path} cargado con {len(df)} filas válidas.")
        print(f"🧾 Columnas detectadas: {list(df.columns)}")

        # Normalizar nombres de columnas
        df.columns = [c.strip().lower() for c in df.columns]

        # Eliminar filas completamente vacías
        df = df.dropna(how="all")

        return df
    except Exception as e:
        print(f"❌ Error al leer CSV: {e}")
        return pd.DataFrame()
