import matplotlib.pyplot as plt
import numpy as np
import cv2

def histograma(image):
  # Calculamos el histograma de la imagen
  hist = cv2.calcHist([image], [0], None, [256], [0, 256])
  plt.subplot(2, 2, 3)
  plt.plot(hist, color='gray')
  plt.title("Histograma")
  plt.xlim([0, 256])
  plt.show()


def autoDetect(path):
  # leemos la imagen a color
  image = cv2.imread(path)
  # Umbralizamos la imagen usando el método de Otsu en el canal rojo
  red = image[:, :, 2]
  _, threshold = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  # Aplicamos el filtro media 3 veces
  median = cv2.medianBlur(threshold, 3)
  median = cv2.medianBlur(median, 3)
  median = cv2.medianBlur(median, 3)
  # Aplicamos el filtro min 4 veces
  min = cv2.erode(median, None, iterations=4)
  # Aplicamos el filtro gaussiano 2 veces
  gaussian = cv2.GaussianBlur(min, (3, 3), 0)
  # Aplicamos filtro media
  median = cv2.medianBlur(gaussian, 3)
  median = cv2.medianBlur(median, 3)
  # Aplicamos el filtro max 2 vez
  max = cv2.dilate(median, None, iterations=4)
  # Aplicamos el filtro media
  median = cv2.medianBlur(max, 3)
  median = cv2.medianBlur(median, 3)
  median = cv2.medianBlur(median, 3)
  # Aplicamos sobel
  sobely = cv2.Sobel(median, cv2.CV_64F, 0, 1, ksize=3)
  # Mostramos los bordes sobre la imagen original
  restricted = cv2.bitwise_and(image, image, mask=np.uint8(sobely))
  # Guardamos la imagen umbralizada, restringida y la imagen original de forma temporal
  cv2.imwrite("temp.jpg", median)
  cv2.imwrite("temp2.jpg", image)
  cv2.imwrite("temp3.jpg", restricted)
  return {'image1':"temp2.jpg", 'image2':"temp.jpg", 'image3':"temp3.jpg"}

def prewit(path):
  # leemos la imagen a color
  image = cv2.imread(path)
  # Convertimos la imagen a escala de grises
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # Aplicamos el filtro de Prewitt en el eje x
  prewittx = cv2.filter2D(gray, cv2.CV_64F, np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]))
  # Guardamos la imagen resultante de forma temporal
  cv2.imwrite("temp.jpg", prewittx)
  return "temp.jpg"

def average(path):
  # leemos la imagen a color
  image = cv2.imread(path)
  # Convertimos la imagen a escala de grises
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # Aplicamos el filtro de la media
  average = cv2.blur(gray, (3, 3))
  # Guardamos la imagen resultante de forma temporal
  cv2.imwrite("temp.jpg", average)
  return "temp.jpg"

def otsu(path):
  # leemos la imagen a color
  image = cv2.imread(path)
  # Convertimos la imagen a escala de grises
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # Aplicamos el método de Otsu
  _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  # Guardamos la imagen resultante de forma temporal
  cv2.imwrite("temp.jpg", otsu)
  return "temp.jpg"

def ecualization(path):
  # leemos la imagen a color
  image = cv2.imread(path)
  # Convertimos la imagen a escala de grises
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # Aplicamos la ecualización del histograma
  equalized = cv2.equalizeHist(gray)
  # Guardamos la imagen resultante de forma temporal
  cv2.imwrite("temp.jpg", equalized)
  return "temp.jpg"