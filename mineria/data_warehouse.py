# Step 0 — Importar librerías
import pandas as pd
from pathlib import Path

# Step 1 — Subir el archivo CSV desde tu computadora
archivo = "garantias.csv"

# Step 2 — Leer el CSV en un DataFrame
df = pd.read_csv(archivo)

# Step 3 — Explorar los datos (inspección inicial)
df.head()
#df.info()
#df.describe()

# Step 4 — Limpieza básica de datos
df_limpio = df.dropna()
df_limpio = df_limpio.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df_limpio.info()

# Step 5 — Preparar los datos para un Data Warehouse
df_dw = df_limpio[['fecha', 'producto', 'categoria', 'ventas']]

# Step 6 — Guardar el dataset limpio (listo para el DW)
Path("csv").mkdir(exist_ok=True)
df_dw.to_csv("csv/datos_limpios_dw.csv", index=False)

# Step 1 (Modelo DW) — Cargar el dataset limpio
df_dw = pd.read_csv("csv/datos_limpios_dw.csv")
df_dw["fecha"] = pd.to_datetime(df_dw["fecha"], errors="coerce")
df_dw["ventas"] = pd.to_numeric(df_dw["ventas"], errors="coerce")
df_dw = df_dw.dropna(subset=["fecha", "ventas"])
df_dw.head()

# Step 2 — Crear dimensiones (modelo estrella)
dim_tiempo = (
    df_dw[["fecha"]]
    .drop_duplicates()
    .assign(
        date_id=lambda d: d["fecha"].dt.strftime("%Y%m%d").astype(int),
        anio=lambda d: d["fecha"].dt.year,
        mes=lambda d: d["fecha"].dt.month,
        dia=lambda d: d["fecha"].dt.day
    )[["date_id", "fecha", "anio", "mes", "dia"]]
    .reset_index(drop=True)
)

dim_producto = (
    df_dw[["producto"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_producto["producto_id"] = dim_producto.index + 1
dim_producto = dim_producto[["producto_id", "producto"]]

dim_categoria = (
    df_dw[["categoria"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_categoria["categoria_id"] = dim_categoria.index + 1
dim_categoria = dim_categoria[["categoria_id", "categoria"]]

dim_tiempo.head(), dim_producto.head(), dim_categoria.head()

# Step 3 — Crear tabla de hechos (Fact) con llaves foráneas
map_producto = dict(zip(dim_producto["producto"], dim_producto["producto_id"]))
map_categoria = dict(zip(dim_categoria["categoria"], dim_categoria["categoria_id"]))

fact_ventas = df_dw.copy()
fact_ventas["date_id"] = fact_ventas["fecha"].dt.strftime("%Y%m%d").astype(int)
fact_ventas["producto_id"] = fact_ventas["producto"].map(map_producto)
fact_ventas["categoria_id"] = fact_ventas["categoria"].map(map_categoria)
fact_ventas = fact_ventas[["date_id", "producto_id", "categoria_id", "ventas"]]
fact_ventas.head()

# Step 4 — Cargar el modelo estrella a SQLite (DW real)
import sqlite3
SQLITE_DIR = Path("sqlite")
SQLITE_DIR.mkdir(exist_ok=True)
db_path = SQLITE_DIR / "dw.sqlite"
conn = sqlite3.connect(db_path)

dim_tiempo.to_sql("dim_tiempo", conn, if_exists="replace", index=False)
dim_producto.to_sql("dim_producto", conn, if_exists="replace", index=False)
dim_categoria.to_sql("dim_categoria", conn, if_exists="replace", index=False)
fact_ventas.to_sql("fact_ventas", conn, if_exists="replace", index=False)

conn.close()
db_path

# Step 5 — Consultas analíticas (validación del DW)
conn = sqlite3.connect("sqlite/dw.sqlite")

q1 = """
SELECT p.producto, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_producto p ON p.producto_id = f.producto_id
GROUP BY p.producto
ORDER BY total_ventas DESC;
"""
ventas_por_producto = pd.read_sql_query(q1, conn)

q2 = """
SELECT c.categoria, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_categoria c ON c.categoria_id = f.categoria_id
GROUP BY c.categoria
ORDER BY total_ventas DESC;
"""
ventas_por_categoria = pd.read_sql_query(q2, conn)

q3 = """
SELECT t.anio, t.mes, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_tiempo t ON t.date_id = f.date_id
GROUP BY t.anio, t.mes
ORDER BY t.anio, t.mes;
"""
ventas_por_mes = pd.read_sql_query(q3, conn)

conn.close()
ventas_por_producto, ventas_por_categoria, ventas_por_mes

# Step 6 — Exportar tablas del DW a CSV
CSV_DIR = Path("csv")
CSV_DIR.mkdir(exist_ok=True)
print("Los CSV se guardarán en:", CSV_DIR.resolve())

dim_tiempo.to_csv(CSV_DIR / "dim_tiempo.csv", index=False)
dim_producto.to_csv(CSV_DIR / "dim_producto.csv", index=False)
dim_categoria.to_csv(CSV_DIR / "dim_categoria.csv", index=False)
fact_ventas.to_csv(CSV_DIR / "fact_ventas.csv", index=False)

["dim_tiempo.csv", "dim_producto.csv", "dim_categoria.csv", "fact_ventas.csv"]