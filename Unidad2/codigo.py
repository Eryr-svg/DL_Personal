#datos
x = [1.50, 1.60, 1.70] #altura de los niños
y = [50, 60, 65] #peso de los niños
n = len(x)

#caulcular las sumatorias
sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum(x[i]*y[i] for i in range(n))
sum_x2 = sum(xi**2 for xi in x)

#calcular pendiente(m)
m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)

#calcular intercepto(b)
b = (sum_y - m*sum_x) / n

print("Pendiente m = ", m)
print("Intercepto b = ", b)

#prediccion
altura_nueva = 1.65
peso_predicho = m*altura_nueva + b

print("Peso estimado para altura: ", altura_nueva, " = ", peso_predicho, " kg")