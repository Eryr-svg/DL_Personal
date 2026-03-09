# Step 1 — Importar librerías
# Librería para manipulación y análisis de datos en forma de tablas
import pandas as pd

# Librería para cálculos numéricos y manejo de arreglos
import numpy as np

# Algoritmo de clustering KMeans
from sklearn.cluster import KMeans

# Herramienta para normalizar datos
from sklearn.preprocessing import StandardScaler

# Librería para crear gráficos
import matplotlib.pyplot as plt

# Step 2 — Cargar el dataset
# Cargar el dataset desde el archivo local titanic.csv
df = pd.read_csv("titanic.csv")

# Mostrar las primeras filas del dataset
df.head()

# Step 3 — Explorar los datos
# Muestra información general del dataset
df.info()

# Muestra estadísticas descriptivas de las variables numéricas
df.describe()

# Step 4 — Revisar valores nulos
# Cuenta Los valores nulos en cada columna
df.isnull().sum()

# Step 5 — Eliminar columnas innecesarias
# Eliminar columnas que no aportan al análisis
df = df.drop(['PassengerId','Name','Ticket','Cabin'], axis=1)

# Step 6 — Convertir variables categóricas
# Convertir la columna Sex a valores numéricos
df['Sex'] = df['Sex'].map({'male':0, 'female':1})

# Step 7 — Rellenar valores faltantes
# Reemplazar valores nulos en Age con el promedio de la columna
df['Age'].fillna(df['Age'].mean(), inplace=True)

# Reemplazar valores nulos en Embarked con el valor más frecuente
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Step 8 — Convertir Embarked a números
# Convertir valores de texto a números
df['Embarked'] = df['Embarked'].map({'S':0,'C':1,'Q':2})

# Step 9 — Seleccionar variables
# Seleccionar columnas que se usarán en el clustering
X = df[['Pclass','Age','Fare','Sex']]

# Step 10 — Normalizar datos
# Crear objeto para normalizar datos
scaler = StandardScaler()

# Aplicar normalización a las variables
X_scaled = scaler.fit_transform(X)

# Step 11 — Aplicar KMeans
# Seleccionar variables para clustering
X = df[['Pclass', 'Age', 'Fare', 'Sex']].copy()
# Convertir Sex a 0/1 de forma robusta
# Casos soportados: "male/female", "Male/Female", "M/F", 0/1, etc.
def sex_to_num(v):
    if pd.isna(v):
        return np.nan
    s = str(v).strip().lower()
    if s in ['male', 'm', '0', 'man', 'hombre']:
        return 0
    if s in ['female', 'f', '1', 'woman', 'mujer']:
        return 1
    return np.nan # cualquier valor raro

X['Sex'] = X['Sex'].apply(sex_to_num)
# Rellenar nulos numéricos y eliminar filas todavía incompletas
X['Age'] = pd.to_numeric(X['Age'], errors='coerce').fillna(X['Age'].mean())
X['Fare'] = pd.to_numeric(X['Fare'], errors='coerce').fillna(X['Fare'].mean())
X['Pclass'] = pd.to_numeric(X['Pclass'], errors='coerce')
X = X.dropna() # elimina solo lo que quedó imposible de convertir

# Verificación: asegurar que sí hay filas
print("Filas disponibles para clustering:", len(X))

# Normalizar y aplicar KMeans
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Guardar clusters en el DF original (alineado por índice)
df.loc[X.index, 'Cluster'] = clusters

# Step 12 — Visualizar clusters
# Crear gráfico de dispersión
plt.scatter(df['Age'], df['Fare'], c=df['Cluster'])

# Etiqueta eje X
plt.xlabel("Edad")
# Etiqueta eje Y
plt.ylabel("Tarifa")
# Titulo del grafico
plt.title("Clusters de pasajeros del Titanic")
# Mostrar grafico
plt.show()

# Step 13 — Interpretar resultados
# Calcular promedio de variables por cluster
df.groupby('Cluster').mean()

# Step 14 — Comparar clusters con la supervivencia
# Calcular la tasa promedio de supervivencia por cluster
survival_by_cluster = df.groupby('Cluster')['Survived'].mean()

# Mostrar los resultados
print(survival_by_cluster)

# Calculer supervivencia promedio por cluster
survival_by_cluster = df.groupby('Cluster')['Survived'].mean()
# Convertir a porcentaje
survival_percentage = survival_by_cluster * 100
# Crear gráfico de barras
survival_percentage.plot(kind='bar')
# Etiquetas
plt.xlabel("Cluster")
plt.ylabel("Supervivencia (%)")
plt.title("Porcentaje de supervivencia por cluster")
# Mostrar valores encima de las barras
for i, v in enumerate(survival_percentage):
    plt.text(i, v + 1, f"{v:.1f}%", ha='center')
plt.show()