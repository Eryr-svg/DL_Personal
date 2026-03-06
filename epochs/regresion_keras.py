import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

x_train = np.array([1.2, 2.5, 0.8, 3.1, 4.2, 5.7, 2.1, 3.4, 4.8, 6.3, 1.5, 3.9, 2.8, 4.1, 7.2, 3.3, 4.5, 1.9, 5.2, 2.4, 3.6, 6.8, 4.0, 2.9, 5.5])
y_train = np.array([0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1])

#definicion del modelo (1 neurona, activacion sigmoide para binario)
model = keras.Sequential([
    layers.Dense(1, input_shape=(1,), activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

print("Iniciando el modelo automatico...")

model.fit(x_train, y_train, epochs=100, verbose=0)

print("Entrenamiento completo")

horas_nuevas = np.array([4.0])
probabilidad = model.predict(horas_nuevas)
resultado = 1 if probabilidad >= 0.5 else 0

print(f"\nPara {horas_nuevas[0]} horas, la probabilidad de aprobar es: {probabilidad[0][0]}")
print(f"Resultado estimado: {'aprobado' if resultado == 1 else 'Reprobado'}")