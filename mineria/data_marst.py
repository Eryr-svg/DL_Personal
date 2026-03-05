import sqlite3
import pandas as pd
from pathlib import Path

#Conectar al DW
DW_PATH = Path("sqlite") / "dw.sqlite"

if not DW_PATH.exists():
    raise FileNotFoundError("No existe dw.sqlite")

dw_conn = sqlite3.connect(DW_PATH)

dim_tiempo = pd.read_sql_query("SELECT * FROM dim_tiempo;", dw_conn)
dim_producto = pd.read_sql_query("SELECT * FROM dim_producto;", dw_conn)
dim_categoria = pd.read_sql_query("SELECT * FROM dim_categoria;", dw_conn)
fact_ventas = pd.read_sql_query("SELECT * FROM fact_ventas;", dw_conn)

dw_conn.close()

#Construir data mart
fact_dm = (
    fact_ventas
    .merge(dim_tiempo[["date_id", "anio", "mes"]], on="date_id")
)

#Agregacion
fact_ventas_dm_ag = (
    fact_dm
    .groupby(["anio", "mes", "categoria_id"], as_index=False)["ventas"]
    .sum()
    .rename(columns={"ventas": "total_ventas"})
)

#Dimension de tiempo
dim_tiempo_dm = (
    fact_ventas_dm_ag[["anio", "mes"]]
    .drop_duplicates()
    .sort_values(["anio", "mes"])
    .reset_index(drop=True)
)

dim_tiempo_dm["tiempo_id"] = dim_tiempo_dm.index + 1
dim_tiempo_dm = dim_tiempo_dm[["tiempo_id", "anio", "mes"]]

#Dimension de hechos
fact_ventas_dm = fact_ventas_dm_ag.merge(
    dim_tiempo_dm,
    on=["anio", "mes"],
    how="left"
)

fact_ventas_dm = fact_ventas_dm[
    ["tiempo_id", "categoria_id", "total_ventas"]
]

#Guardar data mart
DM_PATH = Path("sqlite") / "data_mart_ventas.sqlite"
dm_conn = sqlite3.connect(DM_PATH)

dim_tiempo_dm.to_sql("dim_tiempo_dm", dm_conn, if_exists="replace", index=False)
dim_categoria.to_sql("dim_categoria", dm_conn, if_exists="replace", index=False)
fact_ventas_dm.to_sql("fact_ventas_dm", dm_conn, if_exists="replace", index=False)

dm_conn.close()

print("Data Mart creado correctamente en:", DM_PATH)