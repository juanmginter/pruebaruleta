from PIL import Image, ImageEnhance, ImageFilter

def redimensionar(captura):

    # Abrir la imagen original
    imagen = Image.open(captura)

    # Definir el nuevo tamaño deseado
    nuevo_ancho = 970
    nuevo_alto = 90

    # Redimensionar la imagen sin pérdida de calidad utilizando LANCZOS
    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    # Aplicar mejoras de contraste
    enhancer = ImageEnhance.Contrast(imagen_redimensionada)
    imagen_redimensionada = enhancer.enhance(1.1)

    # Aumentar el brillo
    brillo = ImageEnhance.Brightness(imagen_redimensionada)
    imagen_redimensionada = brillo.enhance(1.2)

    # Eliminación de ruido
    imagen_redimensionada = imagen_redimensionada.filter(ImageFilter.SMOOTH_MORE)

    # Aplicar nitidez
    imagen_redimensionada = imagen_redimensionada.filter(ImageFilter.SHARPEN)

    # Guardar la imagen redimensionada
    imagen_redimensionada.save('imagen_redimensionada.png')

    # Mostrar la imagen redimensionada (opcional)
    #imagen_redimensionada.show()