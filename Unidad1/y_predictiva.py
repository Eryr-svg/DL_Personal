import values_xwyalpha as values

#!Esto corresponde a cuanto espero que aprenda realmente el pokémon despues de los combates
y_hat = []

#aqui se cambian los ciclos del for por anidados manuales
y_hat = [sum(x_ij * w_j for x_ij, w_j in zip(row, values.w)) for row in values.X]

# print("y_hat =", y_hat)