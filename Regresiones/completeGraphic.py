import matplotlib.pyplot as plt

# --- 1. Extraer los datos ---
ruta_archivo = "practica2_ml.csv"
x = []  # alturas (X)
y = []  # pesos (Y)

try:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        filas_datos = lineas[1:] 
        for fila in filas_datos:
            celdas = fila.strip().split(",")
            x.append(float(celdas[0]))
            y.append(float(celdas[1]))
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{ruta_archivo}'")
    exit()

# Imprimir datos extraídos (estilo extraction.py)
print("Datos extraídos del CSV:")
print("Altura | Peso")
for i in range(len(x)):
    print(f"{x[i]} | {y[i]}")

# --- 2. Calcular la Regresión Lineal ---
n = len(x)
sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum(x[i]*y[i] for i in range(n))
sum_x2 = sum(xi**2 for xi in x)

# Fórmula de la pendiente (m) e intercepto (b)
m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
b = (sum_y - m*sum_x) / n

print(f"\nPendiente m = {m}")
print(f"Intercepto b = {b}")

# --- 3. Predicciones Manuales ---
cantidad = int(input("\n¿Cuántas alturas deseas predecir? "))
nuevas_alturas = []
pesos_predichos = []

for i in range(cantidad):
    alt = float(input(f"Ingresa la altura #{i+1}: "))
    nuevas_alturas.append(alt)
    pesos_predichos.append(m * alt + b)

# --- 4. Mostrar Tabla Completa en Terminal ---
print("\nTabla completa (reales + predicciones)")
print("Altura\tPeso")

# Datos reales
for i in range(len(x)):
    print(f"{x[i]}\t{y[i]}")

# Datos predichos
for i in range(len(nuevas_alturas)):
    print(f"{nuevas_alturas[i]}\t{round(pesos_predichos[i], 2)} (predicho)")

# --- 5. Generar la Gráfica ---

plt.figure(figsize=(10, 6))

# Dibujar puntos reales y predichos
plt.scatter(x, y, color='blue', label='Datos Reales', s=50)
plt.scatter(nuevas_alturas, pesos_predichos, color='red', marker='x', label='Predicciones', s=100)

# Línea de tendencia (usando el rango total de datos para la recta)
todos_x = x + nuevas_alturas
x_linea = [min(todos_x), max(todos_x)]
y_linea = [m * xi + b for xi in x_linea]
plt.plot(x_linea, y_linea, color='green', linestyle='--', label=f'Recta: y={m:.2f}x + {b:.2f}')

# Estética de la gráfica
plt.title('Regresión Lineal: Relación Altura vs Peso')
plt.xlabel('Altura')
plt.ylabel('Peso')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

print("\nGenerando gráfica... Cierra la ventana de la imagen para finalizar el programa.")
plt.show()