import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen en escala de grises
imagen = cv2.imread('creacion.jpeg', 0)

# Crear la figura para los subplots
plt.figure(figsize=(10, 8))

# Mostramos la imagen en escala de grises
plt.subplot(3, 2, 1)
plt.imshow(imagen, cmap='gray')
plt.title('Imagen en Escala de Grises')

# Binarizar la imagen por Otsu
_, imagen_binarizada = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Mostrar la imagen binarizada
plt.subplot(3, 2, 2)
plt.imshow(imagen_binarizada, cmap='gray')
plt.title('Imagen Binarizada')

# Definir el kernel para la erosión
kernel = np.ones((5,5), np.uint8)

# Aplicar la operación de erosión
imagen_erosionada = cv2.erode(imagen_binarizada, kernel, iterations=1)
# Mostrar la imagen erosionada
plt.subplot(3, 2, 3)
plt.imshow(imagen_erosionada, cmap='gray')
plt.title('Imagen Erosionada')

# Aplicar la operación de dilatación
imagen_dilatada = cv2.dilate(imagen_binarizada, kernel, iterations=1)
# Mostrar la imagen dilatada
plt.subplot(3, 2, 4)
plt.imshow(imagen_dilatada, cmap='gray')
plt.title('Imagen Dilatada')

# Aplicar la operación de apertura
imagen_apertura = cv2.morphologyEx(imagen_binarizada, cv2.MORPH_OPEN, kernel)
# Mostrar la imagen con apertura
plt.subplot(3, 2, 5)
plt.imshow(imagen_apertura, cmap='gray')
plt.title('Imagen con Apertura')

# Aplicar la operación de cierre
imagen_cierre = cv2.morphologyEx(imagen_binarizada, cv2.MORPH_CLOSE, kernel)
# Mostrar la imagen con cierre
plt.subplot(3, 2, 6)
plt.imshow(imagen_cierre, cmap='gray')
plt.title('Imagen con Cierre')

# Mostrar todas las imágenes
plt.tight_layout()
plt.show()
