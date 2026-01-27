grad = [0, 0]

for j in range(2):          # columnas
    suma = 0
    for i in range(3):      # filas
        suma = suma + X[i][j] * e[i]
    grad[j] = suma

print("X^T e =", grad)
