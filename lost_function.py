import values_xwyalpha as values
import y_predictiva as yp


#esto para obtener (y-y_hat)2
perdida_individual = [(values.y[i] - yp.y_hat[i])**2 for i in range(len(values.y))]

#La perdida total es la suma de los cuadrados
L =sum(perdida_individual)