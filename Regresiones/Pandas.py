import pandas as pd

#1. Leer los datos con Pandas
ruta_archivo = "practica2_ml.csv"

try:
    df = pd.read_csv(ruta_archivo)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{ruta_archivo}'")
    exit()

# Suponiendo que la primera columna es Altura y la segunda Peso
x = df.iloc[:, 0].astype(float).tolist()
y = df.iloc[:, 1].astype(float).tolist()

print("Datos extraídos del CSV:")
print("Altura | Peso")
for i in range(len(x)):
    print(f"{x[i]} | {y[i]}")

#2. Calcular Regresión Lineal
n = len(x)
sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum(x[i]*y[i] for i in range(n))
sum_x2 = sum(xi**2 for xi in x)

m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
b = (sum_y - m*sum_x) / n

print(f"\nPendiente m = {m}")
print(f"Intercepto b = {b}")

#3. Predicciones
cantidad = int(input("\n¿Cuántas alturas deseas predecir? "))
nuevas_alturas = []
pesos_predichos = []

for i in range(cantidad):
    alt = float(input(f"Ingresa la altura #{i+1}: "))
    nuevas_alturas.append(alt)
    pesos_predichos.append(m * alt + b)

#4. Mostrar resultados
print("\nTabla completa (reales + predicciones)")
print("Altura\tPeso")

for i in range(len(x)):
    print(f"{x[i]}\t{y[i]}")

for i in range(len(nuevas_alturas)):
    print(f"{nuevas_alturas[i]}\t{round(pesos_predichos[i], 2)} (predicho)")