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

#Añadir los datos 5 y 6
nueva_alturas = [1.65, 1.75, 1.90]

#añadir a la tabla
print("\nTabla de datos + regresion")
print("altura\tPeso")

#imprimir los datos reales
for i in range(len(x)):
    print(x[i], "\t", y[i])

#calcular e imprimir nuevamente los datos predichos
for altura in nueva_alturas:
    peso_predicho = m * altura + b
    print(altura, "\t", round(peso_predicho, 2), "(predicho)")