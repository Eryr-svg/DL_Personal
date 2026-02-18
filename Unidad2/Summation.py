from values import x, y, n

#caulcular las sumatorias
sum_x = sum(x)
sum_y = sum(y)
sum_xy = sum(x[i]*y[i] for i in range(n))
sum_x2 = sum(xi**2 for xi in x)