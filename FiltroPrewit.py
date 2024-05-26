import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class Filter:
  
  def __init__(self, image, mask):
    self.image = image
    self.width = image.width
    self.height = image.height
    self.newImage = image.copy()
    self.mask = mask
    self.widthMask = len(mask[0])
    self.heightMask = len(mask)

  def applyFilter(self, N = 1):
    for x in range(1, self.width-1):
      for y in range(1, self.height-1):
        self.applyMask(x, y, N)
    return self.newImage
  
  def applyMask(self, x, y, N ):
    total = 0
    for i in range(self.widthMask):
      for j in range(self.heightMask):
        total += self.image.getpixel((x-1+i, y-1+j)) * self.mask[i][j]
    self.newImage.putpixel((x, y), int(total/N))

  def applyNoise(self, rate = 0.1):
    # Aplicamos un procentaje de ruido
    for x in range(self.width):
      for y in range(self.height):
        if np.random.rand() < rate:
          self.image.putpixel((x, y), 255)
# (self.widthMask*(self.heightMask+N)


def main():
  image = Image.open("pasto3.jpg").convert("L")
  plt.subplot(2, 2, 1)
  plt.imshow(image, cmap='gray')
  plt.title("Imagen original")
  #mask = [[1, 0, -1], [2, 0, -2], [1, 0, -1]] # Sobel
  #mask = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]] # Prewit fila
  #mask = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]] # Prewit columna
  #mask = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]] # Laplaciano
  #mask = [[0, 0, 0], [0, 1, 0], [0, 0, 0]] # identidad
  #mask = [[1, 1, 1], [1, 1, 1], [1, 1, 1]] # promedio
  mask = [[1, 1, 1], [1, 8, 1], [1, 1, 1]] # promedio ponderado, N = 8
  filter = Filter(image, mask)
  # Aplicamos un ruido a la imagen
  filter.applyNoise(rate = 0.3)
  newImage = filter.applyFilter(N=20)
  plt.subplot(2, 2, 2)
  plt.imshow(newImage, cmap='gray')
  plt.title("Imagen filtrada")
  
  # Mostramos El histograma de la imagen original
  plt.subplot(2, 2, 3)
  plt.hist(np.array(filter.image).flatten(), bins=256, range=[0, 256])
  plt.title("Histograma de la imagen original")

  # Mostramos El histograma de la imagen filtrada
  plt.subplot(2, 2, 4)
  plt.hist(np.array(newImage).flatten(), bins=256, range=[0, 256])
  plt.title("Histograma de la imagen filtrada")
  plt.show()
 
if __name__ == "__main__":
  main()