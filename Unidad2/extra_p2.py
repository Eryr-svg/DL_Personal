#datos
x = [1, 3, 4, 2, 1, 7] # Nomina en Manhattan (en cientos de millones)
y = [2, 3, 2.5, 2, 2, 3.5] # Ventas (cientos de miles)
n = len(x) #numero de datos de la matriz de X

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
nomina_nueva = 5
ventas_predichas = m*nomina_nueva + b

print("Formula general Y = ", m, "x  + ", b)
print("Ventas estimadas para nomina: ", nomina_nueva, " = ", ventas_predichas, " cientos de miles")