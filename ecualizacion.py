import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

# Función para ecualizar una imagen
def ecualizar_imagen(input_path, output_path):
    # Leer la imagen en escala de grises
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: No se pudo abrir la imagen en la ruta {input_path}")
        return

    # Obtener el valor mínimo y máximo de intensidad en la imagen
    f_min = np.min(img)
    f_max = np.max(img)
    
    # Definir los valores de MIN y MAX para la ecualización
    MIN = 0
    MAX = 50
    
    # Aplicar la fórmula de ecualización
    #img_eq = ((img - f_min) / (f_max - f_min)) * (MAX - MIN) + MIN
    img_eq = (f_max - f_min) * img + f_min
    img_eq = img_eq.astype(np.uint8)  # Convertir a uint8
    print(np.max(img_eq))
    print(np.min(img_eq))
    
    # mostramos las dos imágenes
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title("Imagen original")
    plt.subplot(1, 2, 2)
    # indicamos que los valores de intensidad están en el rango 0-255
    plt.imshow(img_eq, cmap='gray', vmin=0, vmax=255)
    plt.title("Imagen ecualizada")
    plt.show()

    # Guardar la imagen ecualizada
    """ cv2.imwrite(output_path, img_eq)
    print(f"Imagen ecualizada guardada en {output_path}") """

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
    input_image_path = 'pasto3.jpg'  # Reemplaza con la ruta de tu imagen
    output_image_path = 'imagen_ecualizada.jpg'  # Reemplaza con la ruta de la imagen de salida

    # Llamar a la función para ecualizar la imagen
    #ecualizar_imagen(input_image_path, output_image_path)

    # Cargar la imagen
    imagen = Image.open(input_image_path)
    ecualizacion_histograma(imagen)

if __name__ == "__main__":
    main()
