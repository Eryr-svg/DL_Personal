import pandas as pd

df = pd.read_csv("garantias.csv")

df.head()
df.info()
df.describe()

df_limpio = df.dropna()

df_limpio = df_limpio.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df_limpio.info()

df_dw = df_limpio[["fecha", "producto", "categoria", "ventas"]]

df_dw.to_csv("datos_limpios_dw.csv", index=False)

#===========================================
#PARTE 2, ARCHIVO EJERCICIO_1 EN CLASSROOM
#===========================================

df_dw = pd.read_csv("datos_limpios_dw.csv")

df_dw["fecha"] = pd.to_datetime(df_dw["fecha"], errors="coerce")
df_dw["ventas"] = pd.to_datetime(df_dw["ventas"], errors="coerce")

df_dw = df.dropna(subset=["fecha", "ventas"])
df_dw.head()

dim_tiempo = (
df_dw[["fecha"]] # seleccionar la columna "fecha" del DataFrame base
.drop_duplicates() # eliminar fechas repetidas
.assign(
date_id=lambda d: d["fecha"].dt.strftime("%Y%m%d").astype(int),
anio=lambda d: d["fecha"].dt.year, # extraer el año de la fecha
mes=lambda d: d["fecha"].dt.month, # extraer el mes de la fecha
dia=lambda d: d["fecha"].dt.day # extraer el día de la fecha
)[["date_id", "fecha", "anio", "mes", "dia"]] # reordenar las columnas de la di
.reset_index(drop=True) # reiniciar el índice para que sea consecutivo
)
# Dimensión Producto
dim_producto = (
df_dw[["producto"]]
.drop_duplicates()
.reset_index(drop=True) # Reiniciar el índice
)
# Crear un identificador único para cada producto
dim_producto["producto_id"] = dim_producto.index + 1
# Reordenar las columnas
dim_producto = dim_producto[["producto_id", "producto"]]
# Dimensión Cliente
dim_cliente = (
df_dw[["cliente"]]
.drop_duplicates()
.reset_index(drop=True)
)
dim_cliente["cliente_id"] = dim_cliente.index + 1
dim_cliente = dim_cliente[["cliente_id", "cliente"]]
# Mostrar las primeras filas de cada dimensión creada
dim_tiempo.head(), dim_producto.head(), dim_cliente.head()

map_producto = dict(zip(dim_producto["producto"], dim_producto["producto_id"]))
# 2
map_cliente = dict(zip(dim_cliente["cliente"], dim_cliente["cliente_id"]))
# --- CREAR TABLA DE HECHOS (FACT_VENTAS)
# Crear una copia del DataFrame base para no modificar df_dw
fact_ventas = df_dw.copy()
# Crear la clave foránea date_id a partir de la fecha
fact_ventas["date_id"] = fact_ventas["fecha"].dt.strftime("%Y%m%d").astype(int)
# Reemplazar el nombre del producto por su producto_id
fact_ventas["producto_id"] = fact_ventas["producto"].map(map_producto)
fact_ventas["cliente_id"] = fact_ventas["cliente"].map(map_cliente)
# --- SELECCIONAR SOLO LAS COLUMNAS DE LA TABLA DE HECHOS
# 3
fact_ventas = fact_ventas[["date_id", "producto_id", "cliente_id", "ventas"]]
fact_ventas.head()

import sqlite3

db_path = "dw.sqlite"

conn = sqlite3.connect(db_path)

dim_tiempo.to_sql("dim_tiempo", conn, if_exists="replace", index=False)
dim_producto.to_sql("dim_producto", conn, if_exists="replace", index=False)
dim_cliente.to_sql("dim_cliente", conn, if_exists="replace", index=False)

fact_ventas.to_sql("fact_ventas", conn, if_exists="replace", index=False)

conn.close()

db_path

conn = sqlite3.connect("dw.sqlite")

q1 = """
SELECT p.producto, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_producto p ON p.producto_id = f.producto_id
GROUP BY p.producto
ORDER BY total_ventas DESC;
"""
ventas_por_producto = pd.read_sql_query(q1, conn) # Ejecutar la consulta y guardar
# Consulta 2: Obtener total de ventas por cliente
q2 = """
SELECT c.cliente, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_cliente c ON c.cliente_id = f.cliente_id
GROUP BY c.cliente
ORDER BY total_ventas DESC;
"""
ventas_por_cliente = pd.read_sql_query(q2, conn)
# Ventas por mes
q3 = """
SELECT t.anio, t.mes, SUM(f.ventas) AS total_ventas
FROM fact_ventas f
JOIN dim_tiempo t ON t.date_id = f.date_id
GROUP BY t.anio, t.mes
ORDER BY t.anio, t.mes;
"""
ventas_por_mes = pd.read_sql_query(q3, conn)
conn.close()
# Mostrar los resultados obtenidos
ventas_por_producto, ventas_por_cliente, ventas_por_mes

dim_tiempo.to_csv("dim_tiempo.csv", index=False)
# Exporta la dimensión de producto a un archivo CSV
dim_producto.to_csv("dim_producto.csv", index=False)
# Exporta la dimensión de cliente a un archivo CSV
dim_cliente.to_csv("dim_cliente.csv", index=False)
# Exporta la tabla de hechos de ventas a un archivo CSV
fact_ventas.to_csv("fact_ventas.csv", index=False)
# Lista de los archivos CSV generados
# Útil para validación, logging o procesamiento posterior
["dim_tiempo.csv", "dim_producto.csv", "dim_cliente.csv", "fact_ventas.csv"]