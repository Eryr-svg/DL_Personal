from extraction import x, y, nuevas_alturas, peso_predicho, m, b
import matplotlib.pyplot as plt
import numpy as np

#crear la grafica
plt.figure(figsize=(10,6))

#Grafica de untos reales
plt.scatter(x, y, color="blue", label="datos reales", s=50, alpha=0.7)

#Grafica puntos predichos
plt.scatter(nuevas_alturas, peso_predicho, color="red", label = "Datos predichos", s=50, alpha=0.7, marker="s")

# Crear línea de regresión (para todo el rango de datos)
x_linea = np.linspace(min(x + nuevas_alturas) - 0.1, 
                      max(x + nuevas_alturas) + 0.1, 100)
y_linea = m * x_linea + b
plt.plot(x_linea, y_linea, color='green', linewidth=2, 
         label=f'Línea de regresión: y = {round(m, 4)}x + {round(b, 4)}')

# Personalizar la gráfica
plt.xlabel('Altura', fontsize=12)
plt.ylabel('Peso', fontsize=12)
plt.title('Regresión Lineal - Altura vs Peso', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

# Mostrar la gráfica
plt.tight_layout()
plt.show()

# Mostrar ecuación y estadísticas
print("\n" + "="*50)
print("RESUMEN DEL MODELO")
print("="*50)
print(f"Ecuación de regresión: y = {round(m, 4)}x + {round(b, 4)}")
print(f"Donde:")
print(f"  y = peso predicho")
print(f"  x = altura")
print(f"  Pendiente (m) = {round(m, 4)}")
print(f"  Intercepto (b) = {round(b, 4)}")