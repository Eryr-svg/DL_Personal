import values_xwyalpha as values
import y_predictiva as yp
import errorvector as evector
import errortotal as errort
import ajuste_transpuesta as at
import ajuste_pesos as ap
import nueva_prediccion as np
import nuevo_vectorerror_errortotal as net
import lost_function as lf

print("y_hat =", yp.y_hat)
print("error vector", evector.e)
print("ErrorTotal1 =", errort.ErrorTotal1)
print("Transpuesta = ", at.grad)
print("Nuevos pesos = ", ap.w)
print("y_hat2 = ", np.y_hat2)
print("error nuevo = ", net.e2)
print("ErrorTotal2 = ", lf.L2)
# print("Correccion de pesos = ", at.grad)
# print("Correccion/disminucion del error total = ", ap.w)
# print("Nueva iteracion = ", np.y_hat2)
# print("Nuevo error total = ", net.ErrorTotal2)
# print("Funcion de perdida L inicial = ", lf.L1)
# print("Funcion de perdida L final = ", lf.L2)