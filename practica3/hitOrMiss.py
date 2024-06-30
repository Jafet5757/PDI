import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from skimage import morphology, io, color


def hit_or_miss(image, struct_element1, struct_element2):
    """
    Aplica la transformada hit-or-miss a una imagen binaria.

    Args:
    image (numpy.ndarray): Imagen binaria de entrada.
    struct_element1 (numpy.ndarray): Elemento estructurante para el 'hit'.
    struct_element2 (numpy.ndarray): Elemento estructurante para el 'miss'.

    Returns:
    numpy.ndarray: Imagen resultado después de aplicar la transformada hit-or-miss.
    """
    
    # Erosión con el primer elemento estructurante (hit)
    erosion1 = cv2.erode(image, struct_element1)
    
    # Invertir la imagen
    inverted_image = cv2.bitwise_not(image)
    
    # Erosión con el segundo elemento estructurante (miss) en la imagen invertida
    erosion2 = cv2.erode(inverted_image, struct_element2)
    
    # Intersección de las dos erosiones
    hit_or_miss_result = cv2.bitwise_and(erosion1, erosion2)
    
    return hit_or_miss_result

def adelgazamiento(binary, struct_element1, struct_element2):
  # Invertir la imagen binarizada (adelgazamiento se hace sobre objetos negros sobre fondo blanco)
    binary = cv2.bitwise_not(binary)

    # Definir el kernel estructurante para las operaciones morfológicas
    kernel = np.ones((3, 3), np.uint8)
    
    # Inicializar la imagen del resultado del adelgazamiento
    thin = np.zeros(binary.shape, np.uint8)

    # Aplicar el adelgazamiento
    while True:
        # Inicializar las imágenes para los pases
        prev = thin.copy()
        eroded = cv2.erode(binary, kernel, iterations=1)
        temp = cv2.dilate(eroded, kernel, iterations=1)
        temp = cv2.subtract(binary, temp)
        thin = cv2.bitwise_or(thin, temp)
        binary = eroded.copy()

        # Condición de salida
        if cv2.countNonZero(prev - thin) == 0:
            break

    return thin

def engrosamiento(binary, struct_element1, struct_element2, k=3):
  # Definir el kernel estructurante para las operaciones morfológicas
    kernel = np.ones((3, 3), np.uint8)
    
    # Inicializar la imagen del resultado del engrosamiento
    thick = np.zeros(binary.shape, np.uint8)
    c = 0

    # Aplicar el engrosamiento
    while c < k:
        # Inicializar las imágenes para los pases
        prev = thick.copy()
        dilated = cv2.dilate(binary, kernel, iterations=1)
        temp = cv2.subtract(dilated, binary)
        thick = cv2.bitwise_or(thick, temp)
        binary = thick.copy()

        c += 1

    return thick

def etiquetar_componentes_conexas(imagen_binaria):
    # Asegurarse de que la imagen es binaria (0 y 255)
    _, imagen_binaria = cv2.threshold(imagen_binaria, 127, 255, cv2.THRESH_BINARY)

    # Etiquetar componentes conexas
    num_labels, labels_im = cv2.connectedComponents(imagen_binaria)
    
    # Crear una imagen a color para visualizar mejor las etiquetas
    labels_im_colored = cv2.applyColorMap((labels_im * 255 / num_labels).astype(np.uint8), cv2.COLORMAP_JET)

    return num_labels, labels_im, labels_im_colored

def rotate_structural_element(element):
    """
    Rotates a structural element (kernel) 90 degrees counterclockwise.
    
    Parameters:
    element (numpy.ndarray): The original 2D numpy array representing the structural element.
    
    Returns:
    numpy.ndarray: The rotated structural element.
    """
    # Ensure the element is a numpy array
    element = np.array(element)
    
    # Rotate the element 90 degrees counterclockwise
    rotated_element = np.rot90(element, k=1)
    
    return rotated_element

def esqueleto(binary, struct_element1, struct_element2):

    # Invertir la imagen binarizada (esqueleto se obtiene de objetos blancos sobre fondo negro)
    binary = cv2.bitwise_not(binary)

    # Inicializar el kernel estructurante para la operación de erosión
    kernel = np.ones((3, 3), np.uint8)
    
    # Inicializar la imagen del esqueleto
    skeleton = np.zeros(binary.shape, np.uint8)

    # Aplicar el esqueleto morfológico
    while True:
        # Erosión
        eroded = cv2.erode(binary, kernel, iterations=1)
        # Apertura
        opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)

        # Restar la apertura de la erosión para obtener los puntos del esqueleto
        temp = cv2.subtract(eroded, opened)
        # Unir los puntos del esqueleto obtenidos hasta ahora
        skeleton = cv2.bitwise_or(skeleton, temp)
        # Actualizar la imagen binaria para la siguiente iteración
        binary = eroded.copy()

        # Verificar si no hay más píxeles blancos para detener el proceso
        if cv2.countNonZero(binary) == 0:
            break

    # Invertir de nuevo la imagen del esqueleto para tener objetos negros sobre fondo blanco
    skeleton = cv2.bitwise_not(skeleton)
    # Negamos la imagen
    skeleton = cv2.bitwise_not(skeleton)

    return skeleton

def esqueleto_libreria(image):
    """ Aplicamos la formula
      adelgazamiento = A - hit_or_miss(A, struct_element1, struct_element2)
     """
    # ejecutamos 4 veces el algoritmo de adelgazamiento
    return morphology.skeletonize(image)

# -----------------------------------------------------

# Cargar la imagen binaria
imagen = cv2.imread('yinyang.jpeg', cv2.IMREAD_GRAYSCALE)
# Convertir la imagen a binaria (umbralizar)
# Esto es necesario ya que la THM se aplica a una imagen binaria
_, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)
# Mostrar la imagen original en un subplot
plt.subplot(2, 3, 1)
plt.imshow(imagen_binaria, cmap='gray')
plt.title('Imagen Binaria')

# Definir los elementos estructurantes
# Estructurante "hit" (se requiere que sea 1 en los lugares deseados)
hit_kernel = np.array([
  [1, 1, 0],
  [1, 0, 0],
  [0, 0, 0]
], dtype=np.uint8)
# Estructurante "miss" (se requiere que sea 0 en los lugares deseados)
miss_kernel = np.array([
  [0, 0, 1],
  [0, 1, 1],
  [1, 1, 1]
], dtype=np.uint8)


hom = hit_or_miss(imagen_binaria, hit_kernel, miss_kernel)
ad = adelgazamiento(imagen_binaria, hit_kernel, miss_kernel)
en = engrosamiento(imagen_binaria, hit_kernel, miss_kernel)
_, labels, labels_colored = etiquetar_componentes_conexas(imagen_binaria)
sk = esqueleto(imagen_binaria, hit_kernel, miss_kernel)
sk_lib = esqueleto_libreria(imagen_binaria)


# Mostrar el resultado de la transformada hit-or-miss
plt.subplot(2, 3, 2)
plt.imshow(hom, cmap='gray')
plt.title('Resultado Hit-or-Miss')

# Mostrar el resultado del adelgazamiento
plt.subplot(2, 3, 3)
plt.imshow(ad, cmap='gray')
plt.title('Resultado Adelgazamiento')

# Mostrar el resultado del engrosamiento
plt.subplot(2, 3, 4)
plt.imshow(en, cmap='gray')
plt.title('Resultado Engrosamiento')

# Mostrar la imagen etiquetada
plt.subplot(2, 3, 5)
plt.imshow(labels_colored)
plt.title('Componentes Conexas')

# Mostrar el esqueleto
plt.subplot(2, 3, 6)
plt.imshow(sk, cmap='gray')
plt.title('Esqueleto')

plt.show()

# Mostrar el esqueleto
plt.subplot(1, 2, 1)
plt.imshow(sk_lib, cmap='gray')
plt.title('Esqueleto por libreria')

# Mostrar el esqueleto
plt.subplot(1, 2, 2)
plt.imshow(sk, cmap='gray') 
plt.title('Esqueleto por algoritmo')

plt.show()
