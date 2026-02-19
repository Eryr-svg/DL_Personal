import matplotlib.pyplot as plt

# --- 1. Extraer los datos ---
ruta_archivo = "practica2_ml.csv"
x = []  # alturas (X)
y = []  # pesos (Y)

# Simulación de lectura (asegúrate de que el archivo exista en tu carpeta)
with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
    filas_datos = lineas[1:] 
    for fila in filas_datos:
        celdas = fila.strip().split(",")
        x.append(float(celdas[0]))
        y.append(float(celdas[1]))

# --- 2. Calcular la Regresión Lineal ---
n = len(x)
sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum(x[i]*y[i] for i in range(n))
sum_x2 = sum(xi**2 for xi in x)

m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
b = (sum_y - m*sum_x) / n

# --- 3. Predicciones ---
cantidad = int(input("\n¿Cuántas alturas deseas predecir? "))
nuevas_alturas = []
pesos_predichos = []

for i in range(cantidad):
    alt = float(input(f"Ingresa la altura #{i+1}: "))
    nuevas_alturas.append(alt)
    pesos_predichos.append(m * alt + b)

# --- 4. Generar la Gráfica ---

# Definimos el tamaño de la figura
plt.figure(figsize=(10, 6))

# Dibujar los puntos reales (en azul)
plt.scatter(x, y, color='blue', label='Datos Reales', s=50)

# Dibujar los puntos predichos (en rojo)
plt.scatter(nuevas_alturas, pesos_predichos, color='red', marker='x', label='Predicciones', s=100)

# Crear la línea de regresión (usamos el rango total de X para la línea)
x_linea = [min(x + nuevas_alturas), max(x + nuevas_alturas)]
y_linea = [m * xi + b for xi in x_linea]
plt.plot(x_linea, y_linea, color='green', linestyle='--', label=f'Línea de Regresión: y={m:.2f}x + {b:.2f}')

# Configuración de etiquetas
plt.title('Regresión Lineal: Altura vs Peso')
plt.xlabel('Altura')
plt.ylabel('Peso')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

# Mostrar la gráfica
print("\nMostrando gráfica...")
plt.show()