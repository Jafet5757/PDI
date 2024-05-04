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

  def applyFilter(self):
    for x in range(1, self.width-1):
      for y in range(1, self.height-1):
        self.applyMask(x, y)
    return self.newImage
  
  def applyMask(self, x, y):
    total = 0
    for i in range(self.widthMask):
      for j in range(self.heightMask):
        total += self.image.getpixel((x-1+i, y-1+j)) * self.mask[i][j]
    self.newImage.putpixel((x, y), int(total/(self.widthMask*self.heightMask)))

def main():
  image = Image.open("tigre.jpeg").convert("L")
  plt.subplot(1, 2, 1)
  plt.imshow(image, cmap='gray')
  plt.title("Imagen original")
  #mask = [[1, 0, -1], [2, 0, -2], [1, 0, -1]] # Sobel
  #mask = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]] # Prewit fila
  #mask = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]] # Prewit columna
  #mask = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]] # Laplaciano
  #mask = [[0, 0, 0], [0, 1, 0], [0, 0, 0]] # identidad
  #mask = [[1, 1, 1], [1, 1, 1], [1, 1, 1]] # promedio
  mask = [[1, 2, 1], [-2, 4, -2], [1, 2, 1]] # promedio ponderado
  filter = Filter(image, mask)
  newImage = filter.applyFilter()
  plt.subplot(1, 2, 2)
  plt.imshow(newImage, cmap='gray')
  plt.title("Imagen filtrada")
  plt.show()

if __name__ == "__main__":
  main()