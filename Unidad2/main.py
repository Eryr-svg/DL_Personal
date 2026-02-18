from values import x, y, n
from Summation import sum_x, sum_y, sum_xy, sum_x2
from Lean import m
from intercept import b
from prediction import nomina_nueva, ventas_predichas

print("Pendiente m = ", m)
print("Intercepto b = ", b)

print("Formula general Y = ", m, "x  + ", b)
print("Ventas estimadas para nomina: ", nomina_nueva, " = ", ventas_predichas, " cientos de miles")