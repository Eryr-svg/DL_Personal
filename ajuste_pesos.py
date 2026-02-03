from values_xwyalpha import w, alpha
from ajuste_transpuesta import grad

for j in range(2):
    w[j] = w[j] + alpha * grad[j]

# print("nuevos pesos w =", w)