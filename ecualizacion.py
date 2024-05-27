import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image



# Función para ecualizar un histograma de una imagen
def ecualizacion_histograma(imagen):
    # Convertir la imagen a escala de grises si no lo está
    if imagen.mode != 'L':
        imagen = imagen.convert('L')
    
    # Convertir la imagen a un array numpy
    imagen_array = np.array(imagen)
    
    # Calcular el histograma
    histograma, _ = np.histogram(imagen_array.flatten(), bins=256, range=[0, 256])
    
    # Calcular la función de distribución acumulativa (CDF)
    cdf = histograma.cumsum()
    
    # Normalizar la CDF
    cdf_normalizada = cdf * (255 / cdf[-1])
    
    # Mapear los valores de los píxeles originales a los nuevos valores
    imagen_ecualizada = np.interp(imagen_array.flatten(), np.arange(256), cdf_normalizada)
    
    # Remodelar la imagen ecualizada a la forma original
    imagen_ecualizada = imagen_ecualizada.reshape(imagen_array.shape)
    
    # Convertir el array numpy de nuevo a una imagen
    imagen_ecualizada = Image.fromarray(np.uint8(imagen_ecualizada))
    
    # Mostrar la imagen original y la imagen ecualizada
    plt.subplot(2, 2, 1)
    plt.imshow(imagen, cmap='gray')
    plt.title("Imagen Original")
    # Mostrar el histograma de la imagen original
    plt.subplot(2, 2, 3)
    plt.hist(imagen_array.flatten(), bins=256, range=[0, 256], color='r', alpha=0.5)
    plt.title("Histograma Original")
    plt.subplot(2, 2, 2)
    plt.imshow(imagen_ecualizada, cmap='gray')
    plt.title("Imagen Ecualizada")
    # Mostrar el histograma de la imagen ecualizada
    plt.subplot(2, 2, 4)
    plt.hist(np.array(imagen_ecualizada).flatten(), bins=256, range=[0, 256], color='r', alpha=0.5)
    plt.title("Histograma Ecualizado")
    plt.show()

def main():
    # Rutas de las imágenes de entrada y salida
    input_image_path = 'pasto2.jpg'  # Reemplaza con la ruta de tu imagen
    output_image_path = 'imagen_ecualizada.jpg'  # Reemplaza con la ruta de la imagen de salida

    # Llamar a la función para ecualizar la imagen
    #ecualizar_imagen(input_image_path, output_image_path)

    # Cargar la imagen
    imagen = Image.open(input_image_path)
    ecualizacion_histograma(imagen)

if __name__ == "__main__":
    main()
