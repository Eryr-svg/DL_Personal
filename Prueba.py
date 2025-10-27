import tensorflow as tf
#separar vectores sin numpy

vector1 = tf.constant([2, 4, 6])
vector2 = tf.constant([8, 10, 12])
vector3 = tf.constant([14, 16, 18])

#funcion 1, donde posiblemente se uso solo dos vectores de los 3
#se usará para poder señalar y ubicar cada vector de manera individual
f1 = tf.constant([vector1, vector2, vector3])