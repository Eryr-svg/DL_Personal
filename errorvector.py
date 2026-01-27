import values_xwyalpha as values
import y_predictiva as yp

e = []

for i in range(3):
    e.append(values.y[i] - yp.y_hat[i])

#print("error e =", e)
