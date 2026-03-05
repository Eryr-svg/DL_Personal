# Step 0 — Importar librerías
import sqlite3
import pandas as pd
from pathlib import Path

# Step 1 — Definir rutas y validar archivos
CSV_DIR = Path("csv")
SQLITE_DIR = Path("sqlite")

CSV_DIR.mkdir(exist_ok=True)
SQLITE_DIR.mkdir(exist_ok=True)

DW_PATH = SQLITE_DIR / "dw.sqlite"
CSV_PATH = CSV_DIR / "garantias.csv"
DM_PATH = SQLITE_DIR / "data_mart_ventas.sqlite"

if not DW_PATH.exists():
    raise FileNotFoundError(f"❌ No se encontró {DW_PATH}. Ejecuta primero el notebook del Data Warehouse.")
if not CSV_PATH.exists():
    raise FileNotFoundError(f"❌ No se encontró {CSV_PATH}. Debe estar en carpeta csv/")

# Step 2 — Leer dimensiones desde el Data Warehouse (dw.sqlite)
conn_dw = sqlite3.connect(DW_PATH)

dim_producto = pd.read_sql_query("SELECT * FROM dim_producto;", conn_dw)
dim_categoria = pd.read_sql_query("SELECT * FROM dim_categoria;", conn_dw)
dim_tiempo = pd.read_sql_query("SELECT * FROM dim_tiempo;", conn_dw)
fact_ventas = pd.read_sql_query("SELECT * FROM fact_ventas;", conn_dw)

conn_dw.close()

dim_producto.head()
dim_tiempo.head()
fact_ventas.head()

# Step 3 — Obtener categorías desde el CSV original (garantias.csv)
df_src = pd.read_csv(CSV_PATH)
df_src.columns = [c.strip().lower() for c in df_src.columns]

cols_necesarias = {"producto", "categoria"}
faltantes = cols_necesarias - set(df_src.columns)
if faltantes:
    raise ValueError(f"Al CSV le faltan columnas necesarias: {faltantes}")

map_prod_cat = (
    df_src[["producto", "categoria"]].dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)
map_prod_cat.head()

# Step 4 — Construir dimensiones del Data Mart
dim_categoria = map_prod_cat[["categoria"]].drop_duplicates().reset_index(drop=True)
dim_categoria["categoria_id"] = dim_categoria.index + 1
dim_categoria = dim_categoria[["categoria_id", "categoria"]]

dim_producto_dm = dim_producto.merge(map_prod_cat, on="producto", how="left")
cat_id_map = dict(zip(dim_categoria["categoria"], dim_categoria["categoria_id"]))
dim_producto_dm["categoria_id"] = dim_producto_dm["categoria"].map(cat_id_map)
dim_producto_dm = dim_producto_dm[["producto_id", "producto", "categoria_id"]]

dim_categoria.head(), dim_producto_dm.head()

# Step 5 — Construir la tabla de hechos del Data Mart
fact_dm = (
    fact_ventas
    .merge(dim_producto_dm[["producto_id", "categoria_id"]], on="producto_id", how="left")
    .merge(dim_tiempo[["date_id", "anio", "mes"]], on="date_id", how="left")
)

sin_categoria = fact_dm["categoria_id"].isna().sum()
print("Registros sin categoría_id:", sin_categoria)

fact_ventas_dm_ag = (
    fact_dm
    .groupby(["anio", "mes", "categoria_id"], as_index=False)["ventas"]
    .sum()
    .rename(columns={"ventas": "total_ventas"})
)

fact_ventas_dm_ag.head()

# Step 6 — Guardar el Data Mart en su propia base (data_mart_ventas.sqlite)
required_cols = {"anio", "mes", "categoria_id", "total_ventas"}
missing = required_cols - set(fact_ventas_dm_ag.columns)
if missing:
    raise ValueError(f"fact_ventas_dm_ag NO tiene columnas requeridas: {missing}")

dim_tiempo_dm = (
    fact_ventas_dm_ag[["anio", "mes"]]
    .drop_duplicates()
    .sort_values(["anio", "mes"])
    .reset_index(drop=True)
)
dim_tiempo_dm["tiempo_id"] = dim_tiempo_dm.index + 1
dim_tiempo_dm = dim_tiempo_dm[["tiempo_id", "anio", "mes"]]

fact_ventas_dm = fact_ventas_dm_ag.merge(dim_tiempo_dm, on=["anio", "mes"], how="left")
fact_ventas_dm = fact_ventas_dm[["tiempo_id", "categoria_id", "total_ventas"]]

dm_conn = sqlite3.connect(DM_PATH)
dm_conn.execute("PRAGMA foreign_keys = ON;")

dim_tiempo_dm.to_sql("dim_tiempo_dm", dm_conn, if_exists="replace", index=False)
dim_categoria.to_sql("dim_categoria", dm_conn, if_exists="replace", index=False)
fact_ventas_dm.to_sql("fact_ventas_dm", dm_conn, if_exists="replace", index=False)

dm_conn.commit()

tablas = pd.read_sql_query("""
    SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
""", dm_conn)
c_tiempo = pd.read_sql_query("SELECT COUNT(*) AS n FROM dim_tiempo_dm;", dm_conn)
c_cat = pd.read_sql_query("SELECT COUNT(*) AS n FROM dim_categoria;", dm_conn)
c_fact = pd.read_sql_query("SELECT COUNT(*) AS n FROM fact_ventas_dm;", dm_conn)

dm_conn.close()
print("OK -> Data Mart creado:", DM_PATH.resolve())
tablas, c_tiempo, c_cat, c_fact

# Step 9 — Cerrar conexión
dm_conn.close()
print("Conexión cerrada.")