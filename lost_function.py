import values_xwyalpha as values
import y_predictiva as yp
import nueva_prediccion as np


#esto para obtener (y-y_hat)2
perdida_individual1 = [(values.y[i] - yp.y_hat[i])**2 for i in range(len(values.y))]
perdida_individual2 = [(values.y[i] - np.y_hat2[i])**2 for i in range(len(values.y))]

#La perdida total es la suma de los cuadrados
L1 =sum(perdida_individual1)

L2 = sum(perdida_individual2)