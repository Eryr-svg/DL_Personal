horas_estudio = [1.2, 2.5, 0.8, 3.1, 4.2, 5.7, 2.1, 3.4, 4.8, 6.3, 1.5, 3.9, 2.8, 4.1, 7.2, 3.3, 4.5, 1.9, 5.2, 2.4, 3.6, 6.8, 4.0, 2.9, 5.5]
resultado_real = [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]

peso = 0.0
bias = 0.0
alpha = 0.1

print("Iniciando entrenamiento manual...")

for epoch in range(10):
    for i in range(len(horas_estudio)):
        x = horas_estudio[i]
        y_real = resultado_real[i]

        #Caulcular la activacion (z = w*x + b)
        z = peso * x + bias

        #Funcion de activacion
        if z >= 0:
            y_pred = 1
        else:
            y_pred = 0

        #calclo del error y actualizacon del peso
        error = y_real - y_pred
        peso = peso + alpha * error * x
        bias = bias + alpha * error

    print(f"Epoca {epoch} finalizado")

print("-"*30)
print(f"Peso final: {peso:.4f}")
print(f"bias final: {bias:.4f}")