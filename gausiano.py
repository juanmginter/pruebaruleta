import cv2
import numpy as np

def redimensionar(captura):
    # Leer imagen con OpenCV
    imagen = cv2.imread(captura)

    # Redimensionar (3x zoom para mejor OCR)
    nuevo_ancho = 970
    nuevo_alto = 90
    imagen = cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_CUBIC)

    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # CLAHE para mejorar contraste local
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gris = clahe.apply(gris)

    # Guardar imagen en escala de grises (EasyOCR maneja bien escala de grises)
    cv2.imwrite('imagen_redimensionada.png', gris)