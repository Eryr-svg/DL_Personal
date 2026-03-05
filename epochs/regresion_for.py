import math

#datos
x = [1.2, 2.5, 0.8, 3.1, 4.2, 5.7, 2.1, 3.4, 4.8, 6.3, 1.5, 3.9, 2.8, 4.1, 7.2, 3.3, 4.5, 1.9, 5.2, 2.4, 3.6, 6.8, 4.0, 2.9, 5.5]
y = [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]

w = 0.0
b = 0.0
lr = 0.1

print ("==MODELO USADO CON FOR==")
print ("Iniciando el entrenamiento manual...")

#Bucle en epocas manualmente
for epochs in range (100):
    for i in range(len(x)):
        z = w*x[i]+b #funcion sigmoide
        prediccion = 1 / (1 + math.exp(-z))

        error = prediccion - y[i]

        w = w-lr * error * x[i]
        b = b - lr * error

    if(epochs + 1) % 20 == 0:
        print(f"Epoca {epochs + 1} finalizado")

print(f"\nModelo final: m={w:4f}, b={b:.4f}")