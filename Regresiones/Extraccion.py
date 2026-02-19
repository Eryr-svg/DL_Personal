#nombre del archivo
ruta_archivo = 'practica2_ml.csv'

#lista para guardar los datos del rango
rango_altura_peso = []

with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()

    #seleccion de las filas (2 y 4)
    #se usa [1:] para saltar e encabezado
    filas_datos = lineas[1:]

    for filas in filas_datos:
        #limipar el espacio y separar por comas
        celdas = filas.strip().split(',')

        #seleccion de las columnas
        #colmna A: niños(indice 0), B: altura (indice 1), C: peso (indice 2)
        altura = celdas[0].strip()
        peso = celdas[1].strip()

        #guardar la pareja de datos
        rango_altura_peso.append([altura, peso])

#imprimir el resultado (simulando lo que se veria en excel)
print("---Datos extraidos (columnas B2:C4) ---")
print("Altura | peso")
for dato in rango_altura_peso:
    print(f"{dato[0]} | {dato[1]}")