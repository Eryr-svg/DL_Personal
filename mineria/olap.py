import sqlite3
import pandas as pd
from pathlib import Path

#Conectar al data mart
DM_PATH = Path("sqlite") / "data_mart_ventas.sqlite"

dm_conn = sqlite3.connect(DM_PATH)

#Crear cubo
cur = dm_conn.cursor()

cur.execute("DROP TABLE IF EXISTS olap_cubo_ventas;")

cur.execute("""
CREATE TABLE olap_cubo_ventas AS
SELECT
    t.anio,
    t.mes,
    c.categoria,
    SUM(f.total_ventas) AS ventas_totales
FROM fact_ventas_dm f
JOIN dim_tiempo_dm t ON t.tiempo_id = f.tiempo_id
JOIN dim_categoria c ON c.categoria_id = f.categoria_id
GROUP BY t.anio, t.mes, c.categoria;
""")

dm_conn.commit()
print("Cubo OLAP creado correctamente.")

#Ejemplo roll-up
pd.read_sql_query("""
SELECT
    categoria,
    SUM(ventas_totales) AS ventas_totales
FROM olap_cubo_ventas
GROUP BY categoria
ORDER BY ventas_totales DESC;
""", dm_conn)