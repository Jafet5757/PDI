import cv2
import numpy as np
import matplotlib.pyplot as plt


# Cargar la imagen en escala de grises
imagen = cv2.imread('creacion.jpeg', cv2.IMREAD_GRAYSCALE)
# Mostrar la imagen original
plt.subplot(2,3,1)
plt.imshow(imagen, cmap='gray')
plt.title('Imagen Original')

# Definir el kernel para la erosión
kernel = np.ones((5,5), np.uint8)
# Aplicar la operación de erosión
imagen_erosionada = cv2.erode(imagen, kernel, iterations = 1)
# Mostrar la imagen erosionada
plt.subplot(2,3,2)
plt.imshow(imagen_erosionada, cmap='gray')
plt.title('Imagen Erosionada')

# Aplicar la operación de dilatación
imagen_dilatada = cv2.dilate(imagen, kernel, iterations = 1)
# Mostrar la imagen dilatada
plt.subplot(2,3,3)
plt.imshow(imagen_dilatada, cmap='gray')
plt.title('Imagen Dilatada')

# Aplicar la operación de apertura
imagen_apertura = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)
# Mostrar la imagen con apertura
plt.subplot(2,3,4)
plt.imshow(imagen_apertura, cmap='gray')
plt.title('Imagen con Apertura')

# Aplicar la operación de cierre
imagen_cierre = cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel)
# Mostrar la imagen con cierre
plt.subplot(2,3,5)
plt.imshow(imagen_cierre, cmap='gray')
plt.title('Imagen con Cierre')
plt.show()


# Aplicamos el gradiente morfológico
imagen_gradiente = cv2.morphologyEx(imagen, cv2.MORPH_GRADIENT, kernel)
# Mostrar la imagen con gradiente morfológico
plt.subplot(2,2,1)
plt.imshow(imagen_gradiente, cmap='gray')
plt.title('Imagen con Gradiente Morfológico')

# Aplicamos el top-hat
imagen_top_hat = cv2.morphologyEx(imagen, cv2.MORPH_TOPHAT, kernel)
# Mostrar la imagen con top-hat
plt.subplot(2,2,2)
plt.imshow(imagen_top_hat, cmap='gray')
plt.title('Imagen con Top-Hat')

# Aplicamos Bottom-hat
imagen_bottom_hat = cv2.morphologyEx(imagen, cv2.MORPH_BLACKHAT, kernel)
# Mostrar la imagen con bottom-hat
plt.subplot(2,2,3)
plt.imshow(imagen_bottom_hat, cmap='gray')
plt.title('Imagen con Bottom-Hat')

# Mostramos la imagen original
plt.subplot(2,2,4)
plt.imshow(imagen, cmap='gray')
plt.title('Imagen Original')

plt.show()