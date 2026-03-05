import pandas as pd
import sqlite3
from pathlib import Path

#Leer csv
archivo = "garantias.csv"
df = pd.read_csv(archivo)

# Normalizar nombres de columnas
df.columns = [c.strip().lower() for c in df.columns]

#Limpieza
# Eliminar nulos
df_limpio = df.dropna()

# Limpiar espacios en columnas tipo texto
df_limpio = df_limpio.apply(
    lambda x: x.str.strip() if x.dtype == "object" else x
)

#Preparar datos DW
df_dw = df_limpio[['fecha', 'producto', 'categoria', 'ventas']]

# Convertir tipos
df_dw["fecha"] = pd.to_datetime(df_dw["fecha"], errors="coerce")
df_dw["ventas"] = pd.to_numeric(df_dw["ventas"], errors="coerce")

df_dw = df_dw.dropna(subset=["fecha", "ventas"])

#Dimension del timempo
dim_tiempo = (
    df_dw[["fecha"]]
    .drop_duplicates()
    .assign(
        date_id=lambda d: d["fecha"].dt.strftime("%Y%m%d").astype(int),
        anio=lambda d: d["fecha"].dt.year,
        mes=lambda d: d["fecha"].dt.month,
        dia=lambda d: d["fecha"].dt.day
    )
    [["date_id", "fecha", "anio", "mes", "dia"]]
    .reset_index(drop=True)
)

#Dimension producto
dim_producto = (
    df_dw[["producto"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_producto["producto_id"] = dim_producto.index + 1
dim_producto = dim_producto[["producto_id", "producto"]]

#Dimension categoria
dim_categoria = (
    df_dw[["categoria"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_categoria["categoria_id"] = dim_categoria.index + 1
dim_categoria = dim_categoria[["categoria_id", "categoria"]]

#Tabla de hechos
# Mapas
map_producto = dict(zip(
    dim_producto["producto"],
    dim_producto["producto_id"]
))

map_categoria = dict(zip(
    dim_categoria["categoria"],
    dim_categoria["categoria_id"]
))

fact_ventas = df_dw.copy()

fact_ventas["date_id"] = fact_ventas["fecha"].dt.strftime("%Y%m%d").astype(int)
fact_ventas["producto_id"] = fact_ventas["producto"].map(map_producto)
fact_ventas["categoria_id"] = fact_ventas["categoria"].map(map_categoria)

fact_ventas = fact_ventas[
    ["date_id", "producto_id", "categoria_id", "ventas"]
]

#Guardar en SQLite
SQLITE_DIR = Path("sqlite")
SQLITE_DIR.mkdir(exist_ok=True)

db_path = SQLITE_DIR / "dw.sqlite"
conn = sqlite3.connect(db_path)

dim_tiempo.to_sql("dim_tiempo", conn, if_exists="replace", index=False)
dim_producto.to_sql("dim_producto", conn, if_exists="replace", index=False)
dim_categoria.to_sql("dim_categoria", conn, if_exists="replace", index=False)
fact_ventas.to_sql("fact_ventas", conn, if_exists="replace", index=False)

conn.close()

print("DW creado correctamente en:", db_path)