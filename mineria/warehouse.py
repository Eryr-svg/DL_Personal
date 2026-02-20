# =========================
# Step 0 — Importar librerías
# =========================
import pandas as pd
import sqlite3

# =========================
# Step 1 — Definir archivo CSV
# =========================
archivo = "garantias.csv"

# =========================
# Step 2 — Leer el CSV
# =========================
df = pd.read_csv(archivo)

# =========================
# Step 3 — Exploración inicial
# =========================
df.head()
# df.info()
# df.describe()

# =========================
# Step 4 — Limpieza básica
# =========================
df_limpio = df.dropna()

df_limpio = df_limpio.apply(
    lambda x: x.str.strip() if x.dtype == "object" else x
)

df_limpio.info()

# =========================
# Step 5 — Preparar datos para DW
# =========================
df_dw = df_limpio[['fecha', 'producto', 'cliente', 'ventas']]

# =========================
# Step 6 — Guardar dataset limpio
# =========================
df_dw.to_csv("datos_limpios_dw.csv", index=False)

# =====================================================
# MODELO DE DATA WAREHOUSE
# =====================================================

# =========================
# Step 1 — Cargar dataset limpio
# =========================
df_dw = pd.read_csv("datos_limpios_dw.csv")

df_dw["fecha"] = pd.to_datetime(df_dw["fecha"], errors="coerce")
df_dw["ventas"] = pd.to_numeric(df_dw["ventas"], errors="coerce")

df_dw = df_dw.dropna(subset=["fecha", "ventas"])
df_dw.head()

# =========================
# Step 2 — Crear dimensiones
# =========================

# Dimensión Tiempo
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

# Dimensión Producto
dim_producto = (
    df_dw[["producto"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_producto["producto_id"] = dim_producto.index + 1
dim_producto = dim_producto[["producto_id", "producto"]]

# Dimensión Cliente
dim_cliente = (
    df_dw[["cliente"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_cliente["cliente_id"] = dim_cliente.index + 1
dim_cliente = dim_cliente[["cliente_id", "cliente"]]

# =========================
# Step 3 — Crear tabla de hechos
# =========================

map_producto = dict(zip(dim_producto["producto"], dim_producto["producto_id"]))
map_cliente = dict(zip(dim_cliente["cliente"], dim_cliente["cliente_id"]))

fact_ventas = df_dw.copy()

fact_ventas["date_id"] = fact_ventas["fecha"].dt.strftime("%Y%m%d").astype(int)
fact_ventas["producto_id"] = fact_ventas["producto"].map(map_producto)
fact_ventas["cliente_id"] = fact_ventas["cliente"].map(map_cliente)

fact_ventas = fact_ventas[["date_id", "producto_id", "cliente_id", "ventas"]]
fact_ventas.head()

# =========================
# Step 4 — Cargar DW en SQLite
# =========================
db_path = "dw.sqlite"
conn = sqlite3.connect(db_path)

dim_tiempo.to_sql("dim_tiempo", conn, if_exists="replace", index=False)
dim_producto.to_sql("dim_producto", conn, if_exists="replace", index=False)
dim_cliente.to_sql("dim_cliente", conn, if_exists="replace", index=False)
fact_ventas.to_sql("fact_ventas", conn, if_exists="replace", index=False)

conn.close()

# =========================
# Step 5 — Consultas analíticas
# =========================
conn = sqlite3.connect("dw.sqlite")

q1 = """
SELECT p.producto, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_producto p ON p.producto_id = f.producto_id
GROUP BY p.producto
ORDER BY total_ventas DESC;
"""
ventas_por_producto = pd.read_sql_query(q1, conn)

q2 = """
SELECT c.cliente, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_cliente c ON c.cliente_id = f.cliente_id
GROUP BY c.cliente
ORDER BY total_ventas DESC;
"""
ventas_por_cliente = pd.read_sql_query(q2, conn)

q3 = """
SELECT t.anio, t.mes, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_tiempo t ON t.date_id = f.date_id
GROUP BY t.anio, t.mes
ORDER BY t.anio, t.mes;
"""
ventas_por_mes = pd.read_sql_query(q3, conn)

conn.close()

ventas_por_producto, ventas_por_cliente, ventas_por_mes

# =========================
# Step 6 — Exportar tablas a CSV
# =========================
dim_tiempo.to_csv("dim_tiempo.csv", index=False)
dim_producto.to_csv("dim_producto.csv", index=False)
dim_cliente.to_csv("dim_cliente.csv", index=False)
fact_ventas.to_csv("fact_ventas.csv", index=False)