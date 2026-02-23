import openpyxl

# --- 1. Extraer los datos con Openpyxl ---
ruta_archivo = "practica2_ml.xlsx"  # Asegúrate de que sea .xlsx
x = []  # alturas (X)
y = []  # pesos (Y)

try:
    # Cargar el libro y la hoja activa
    wb = openpyxl.load_workbook(ruta_archivo, data_only=True)
    hoja = wb.active

    # Iterar sobre las filas (asumiendo que la fila 1 son encabezados)
    # min_row=2 para saltar el encabezado
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        if fila[0] is not None and fila[1] is not None:
            x.append(float(fila[0]))
            y.append(float(fila[1]))
            
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{ruta_archivo}'")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el Excel: {e}")
    exit()

# Imprimir datos extraídos
print("Datos extraídos del Excel:")
print("Altura | Peso")
for i in range(len(x)):
    print(f"{x[i]} | {y[i]}")

# --- 2. Calcular la Regresión Lineal ---
n = len(x)
if n == 0:
    print("No hay datos para procesar.")
    exit()

sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum(x[i] * y[i] for i in range(n))
sum_x2 = sum(xi**2 for xi in x)

# Cálculo de pendiente (m) e intercepto (b) usando LaTeX para referencia:
# m = \frac{n\sum xy - \sum x \sum y}{n\sum x^2 - (\sum x)^2}
m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
b = (sum_y - m * sum_x) / n

print(f"\nPendiente m = {m}")
print(f"Intercepto b = {b}")

# --- 3. Predicciones Manuales ---
try:
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

except ValueError:
    print("Error: Por favor ingresa solo números válidos.")