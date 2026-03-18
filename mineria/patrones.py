import csv
from collections import defaultdict

transacciones = defaultdict(list)

with open("transacciones.csv", newline="") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        transacciones[fila["transaccion"]].append(fila["producto"])

lista_transacciones = list(transacciones.values())

total = len(lista_transacciones)

A = "pan"
B = "leche"

conteo_A = 0
conteo_B = 0
conteo_AyB = 0

for t in lista_transacciones:
  if A in t:
    conteo_A += 1
  if B in t:
    conteo_B += 1
  if A in t and B in t:
    conteo_AyB += 1

soporte = conteo_AyB / total
confianza = conteo_AyB / conteo_A
lift = confianza / (conteo_B / total)

print("Regla:", A, "->", B)
print("Total de transacciones:", total)
print("Support:", soporte)
print("Confidence:", confianza)
print("Lift:", lift)