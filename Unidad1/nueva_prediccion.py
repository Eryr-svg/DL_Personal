from values_xwyalpha import X, w, y

y_hat2 = []

for i in range(3):
    valor = 0
    for j in range(2):
        valor = valor + X[i][j] * w[j]
    y_hat2.append(valor)