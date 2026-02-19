import math

from Summation import sum_x, sum_y, sum_xy, sum_x2, sum_y2
from values import n

#calculo de r
numerador = n*sum_xy - (sum_x*sum_y)
den_x = n*sum_x2 - (sum_x**2)
den_y = n*sum_y2 - (sum_y**2)

r = numerador / math.sqrt(den_x*den_y)

#coeficent
r2 = r**2