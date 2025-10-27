import numpy as np
import matplotlib as plt

#1 se definen los vetores
x1 = np.array([0.5, 0.2, 0.1])
x2 = np.array([0.9, 0.4, 0.7])
x3 = np.array([0.3, 0.8, 0.5])

#1.1 matriz con las 3 entradas
x = np.vstack([x1, x2, x3])

#2 definir la mtriz de pesos y sesgos (bias)
w = np.array([
    [0.2, 0.5, 0.3],
    [0.4, 0.1, 0.6],
    [0.7, 0.8, 0.2]
])

b = np.array([0.1, 0.2, 0.3]) #ejemplo

print("\nMatriz de pesos w:\n", w)
print("\nVector de sesgos b:\n", b)

#3 representar en expresion matricial
r1 = x.dot(w) + b
print("\nResultado de r1 = x*w + b\n", r1)

#4 aplicar una funcion de activacion (capa 1)
def relu():
    return np.maximum(0, x)

a1 = relu(r1)
print("\nResultado tras activacion relu (a1 en capa 1):\n", a1)

#5 sgunda capa oculta (por ejemplo tanh)
w2 = np.array([
    [0.3, 0.7, 0.5],
    [0.6, 0.2, 0.4],
    [0.9, 0.1, 0.8]
])

b2 = np.array([0.05, 0.1, 0.15]) #Ejemplo de bias

r2 = a1.dot(w2) + b2
a2 = np.tanh(r2)

print("\nResultado de capa 2 (a2 por tanh):\n", a2)

#6 mostrar expresion matricial
print("\nExpresion matricial general:")
print("R1 = x*w + b")
print("A1 = relu(r1)")
print("R2 = a1*w2 + b2")
print("A1 = tanh(r2)")