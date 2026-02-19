import matplotlib.pyplot as plt
import numpy as np
#Extraer los datos

ruta_archivo = "practica2_ml.csv"

x = []  # alturas (X)
y = []  # pesos (Y)

with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

    filas_datos = lineas[1:]  # saltar encabezado

    for fila in filas_datos:
        celdas = fila.strip().split(",")

        altura = float(celdas[0])
        peso = float(celdas[1])

        x.append(altura)
        y.append(peso)

print("Datos extraídos del CSV:")
print("Altura | Peso")
for i in range(len(x)):
    print(x[i], "|", y[i])


#calcular la RL

n = len(x)

sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum(x[i]*y[i] for i in range(n))
sum_x2 = sum(xi**2 for xi in x)

m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
b = (sum_y - m*sum_x) / n

print("\nPendiente m =", m)
print("Intercepto b =", b)


#Añadir las predicciones manualmente

cantidad = int(input("\n¿Cuántas alturas deseas predecir? "))

nuevas_alturas = []

for i in range(cantidad):
    altura = float(input(f"Ingresa la altura #{i+1}: "))
    nuevas_alturas.append(altura)


#Mostrar la tabla completa mas las predicciones

print("\nTabla completa (reales + predicciones)")
print("Altura\tPeso")

# datos reales
for i in range(len(x)):
    print(x[i], "\t", y[i])

# datos predichos
for altura in nuevas_alturas:
    peso_predicho = m * altura + b
    print(altura, "\t", round(peso_predicho, 2), "(predicho)")