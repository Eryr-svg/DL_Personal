horas_estudo = [1, 2, 3, 4, 5, 6]
resultado_real = [0, 0, 0, 1, 1, 1]

peso = 0
bias = 0
alpha = 0

for i in range(len(horas_estudo)):
    x = horas_estudo[i]
    y_real = resultado_real[i]

    z = peso * x + bias

    if z>=0:
        y_pred = 1
    else:
        y_pred = 0

    error = y_real - y_pred

    peso = peso + alpha + error * x
    bias = bias + alpha * error

print("Peso: ", peso)
print("Bias: ", bias)