import cv2

def redimensionar(captura):
    # Leer imagen con OpenCV (mantener color)
    imagen = cv2.imread(captura)

    # Escalado 4x para mejor resolución OCR
    factor = 4
    nuevo_ancho = imagen.shape[1] * factor
    nuevo_alto = imagen.shape[0] * factor
    imagen = cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_LINEAR)

    # Desenfoque ligero (recomendado en GitHub issues de EasyOCR)
    imagen = cv2.blur(imagen, (3, 3))

    # Guardar imagen A COLOR (EasyOCR funciona mejor con color)
    cv2.imwrite('imagen_redimensionada.png', imagen)