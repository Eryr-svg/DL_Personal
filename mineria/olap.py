# Step 0 — Importar librerías
import sqlite3
import pandas as pd
from pathlib import Path

# Step 1 — Conectar al Data Mart y validar que exista
DM_PATH = Path("sqlite") / "data_mart_ventas.sqlite"

if not DM_PATH.exists():
    raise FileNotFoundError("No existe data_mart_ventas.sqlite. Ejecuta primero el Ejercicio 2 (Data Mart)")

dm_conn = sqlite3.connect(DM_PATH)
print("OK -> Conectado a:", DM_PATH)

# Step 2 — Validación del Data Mart
pd.read_sql_query("""
    SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
""", dm_conn)

# Step 3 — Creación del Cubo OLAP
cur = dm_conn.cursor()
cur.execute("DROP TABLE IF EXISTS olap_cubo_ventas;")

cur.execute("""
    CREATE TABLE olap_cubo_ventas AS
    SELECT
        t.anio AS anio,
        t.mes AS mes,
        c.categoria AS categoria,
        SUM(f.total_ventas) AS ventas_totales,
        COUNT(*) AS num_registros
    FROM fact_ventas_dm f
    JOIN dim_tiempo_dm t ON t.tiempo_id = f.tiempo_id
    JOIN dim_categoria c ON c.categoria_id = f.categoria_id
    GROUP BY
        t.anio, t.mes, c.categoria;
""")

dm_conn.commit()
print("OK -> Cubo OLAP creado: olap_cubo_ventas")

# Step 4 — Creación de índices
cur.execute("CREATE INDEX IF NOT EXISTS idx_cubo_anio_mes ON olap_cubo_ventas(anio, mes);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_cubo_categoria ON olap_cubo_ventas(categoria);")
dm_conn.commit()
print("Indices creados.")

# Step 5 — Validación del cubo
pd.read_sql_query("""
    SELECT COUNT(*) AS filas_cubo FROM olap_cubo_ventas;
""", dm_conn)

# OLAP 1 — ROLL-UP (Resumir)
pd.read_sql_query("""
    SELECT anio, SUM(ventas_totales) AS ventas_anuales
    FROM olap_cubo_ventas
    GROUP BY anio
    ORDER BY anio;
""", dm_conn)

# OLAP 2 — DRILL-DOWN (Ir a detalle)
pd.read_sql_query("""
    SELECT anio, mes, SUM(ventas_totales) AS ventas_mensuales
    FROM olap_cubo_ventas
    GROUP BY anio, mes
    ORDER BY anio, mes;
""", dm_conn)

# OLAP 3 — SLICE (Filtrar por una dimensión)
pd.read_sql_query("""
    SELECT *
    FROM olap_cubo_ventas
    WHERE anio = 2024
    ORDER BY mes, categoria;
""", dm_conn)

# OLAP 4 — DICE (Filtrar por múltiples condiciones)
pd.read_sql_query("""
    SELECT *
    FROM olap_cubo_ventas
    WHERE anio = 2024
        AND mes BETWEEN 1 AND 6
        AND categoria IN ('electronica', 'papeleria')
    ORDER BY mes, categoria;
""", dm_conn)

# OLAP 5 — PIVOT (Vista tipo "cubo")
df_cubo = pd.read_sql_query("""
    SELECT anio, mes, categoria, ventas_totales
    FROM olap_cubo_ventas
    WHERE anio = 2024;
""", dm_conn)

pivot = df_cubo.pivot_table(
    index="mes",
    columns="categoria",
    values="ventas_totales",
    aggfunc="sum",
    fill_value=0
).sort_index()

pivot

# Step final — Cerrar conexión
dm_conn.close()
print("Conexión cerrada.")