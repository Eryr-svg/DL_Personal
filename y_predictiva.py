
import values_xwyalpha as values

#!Esto corresponde a cuanto espero que aprenda realmente el pokémon despues de los combates
y_hat = []

for i in range(3):          # 3 filas
    valor = 0
    for j in range(2):      # 2 columnas
        valor = valor + values.X[i][j] * values.w[j]
    y_hat.append(valor)

#print("y_hat =", y_hat)