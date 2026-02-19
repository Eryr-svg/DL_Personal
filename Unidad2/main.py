from values import x, y, n
from Summation import sum_x, sum_y, sum_xy, sum_x2, sum_y2
from Lean import m
from intercept import b
from prediction import nomina_nueva, ventas_predichas
from coeficent import r, r2

print("Pendiente m = ", m)
print("Intercepto b = ", b)
print("coeficiente de recolecion r = ", round(r,4))
print("coeficiente de recoleccion r^2 = ", round(r2,4))

print("Formula general Y = ", m, "x  + ", b)
print("Ventas estimadas para nomina: ", nomina_nueva, " = ", ventas_predichas, " cientos de miles")