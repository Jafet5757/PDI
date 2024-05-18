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
    img_eq = ((img - f_min) / (f_max - f_min)) * (MAX - MIN) + MIN
    #img_eq = img_eq.astype(np.uint8)  # Convertir a uint8
    
    # mostramos las dos imágenes
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title("Imagen original")
    plt.subplot(1, 2, 2)
    plt.imshow(img_eq, cmap='gray')
    plt.title("Imagen ecualizada")
    plt.show()

    # Guardar la imagen ecualizada
    cv2.imwrite(output_path, img_eq)
    print(f"Imagen ecualizada guardada en {output_path}")

# Clase para aplicar filtros a una imagen
class Filter:
    def __init__(self, image, mask):
        self.image = image
        self.width = image.width
        self.height = image.height
        self.newImage = image.copy()
        self.mask = mask
        self.widthMask = len(mask[0])
        self.heightMask = len(mask)

    def applyFilter(self, N=0):
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                self.applyMask(x, y, N)
        return self.newImage

    def applyMask(self, x, y, N):
        total = 0
        for i in range(self.widthMask):
            for j in range(self.heightMask):
                total += self.image.getpixel((x - 1 + i, y - 1 + j)) * self.mask[i][j]
        self.newImage.putpixel((x, y), int(total / (self.widthMask * (self.heightMask + N))))

def main():
    # Rutas de las imágenes de entrada y salida
    input_image_path = 'incendio.jpeg'  # Reemplaza con la ruta de tu imagen
    output_image_path = 'imagen_ecualizada.jpg'  # Reemplaza con la ruta de la imagen de salida

    # Llamar a la función para ecualizar la imagen
    ecualizar_imagen(input_image_path, output_image_path)

    # Leer la imagen y convertirla a escala de grises
    image = Image.open(input_image_path).convert("L")
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title("Imagen original")

    # Definir una máscara (ejemplo con filtro Sobel)
    mask = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]  # Sobel

    # Crear el filtro y aplicar la máscara
    filter = Filter(image, mask)
    newImage = filter.applyFilter()
    
    plt.subplot(1, 2, 2)
    plt.imshow(newImage, cmap='gray')
    plt.title("Imagen filtrada")
    plt.show()

if __name__ == "__main__":
    main()
