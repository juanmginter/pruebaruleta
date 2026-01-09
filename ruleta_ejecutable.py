import warnings
warnings.filterwarnings('ignore', message='.*pin_memory.*')
warnings.filterwarnings('ignore', message='.*CUDA.*')

import time
import pyautogui
import easyocr
import pygame
import os
import gausiano

# ===== CONSTANTES =====
UMBRAL_MITADES = 4
UMBRAL_COLORES = 4
UMBRAL_PARIDAD = 4
UMBRAL_DOCENAS = 4
UMBRAL_FILAS = 4

# Inicializar EasyOCR (solo una vez para mejor rendimiento)
reader = easyocr.Reader(['en'])

# COLORES
COLOR_VERDE = '\033[92m'
COLOR_MORADO = '\033[95m'
COLOR_AZUL = '\033[94m'
COLOR_ROJO = '\033[91m'
COLOR_AMARILLO = '\033[93m'
COLOR_CYAN = '\033[96m'
COLOR_DARKCYAN = '\033[36m'
ESTILO_NEGRITA = '\033[1m'
COLOR_RESET = '\033[0m'  # Restablecer el color a su valor predeterminado

# Definir la región de interés (ROI)
x = 1150  # Coordenada X del área de interés
y = 560  # Coordenada Y del área de interés
ancho = 275  # Ancho del área de interés
alto = 30

# Intervalo de tiempo entre capturas (en segundos)
intervalo_captura = 4  # Captura cada 60 segundos

# Función para tomar una captura de pantalla de la región de interés
def tomar_captura():
    captura = pyautogui.screenshot(region=(x, y, ancho, alto))
    return captura

def grabar_captura(captura):
    captura_guardada = captura.save("temp_captura.png")
    return captura_guardada


def obtener_contrario(componente):
    if componente == 0:
        return "IMPAR"
    else:
        return "PAR"

def obtener_contrario_menor_mayor(es_menor):
    if es_menor:
        return "MAYOR"
    else:
        return "MENOR"

def obtener_contrario_color(componente):
    if componente == 'Rojo':
        return "NEGRO"
    else:
        return "ROJO"


def separar_numeros_ruleta(texto):
    """Separa números concatenados en números de ruleta (0-36)"""
    numeros = []
    i = 0
    while i < len(texto):
        # Intentar tomar 2 dígitos primero
        if i + 1 < len(texto):
            dos_digitos = int(texto[i:i+2])
            if dos_digitos <= 36:
                numeros.append(dos_digitos)
                i += 2
                continue
        # Si no, tomar 1 dígito
        numeros.append(int(texto[i]))
        i += 1
    return numeros


def extraer_numeros_de_texto(texto_ocr):
    """Extrae números de ruleta del texto OCR, separando números concatenados"""
    numeros = []
    for palabra in texto_ocr.split():
        if palabra.isdigit():
            if len(palabra) <= 2 and int(palabra) <= 36:
                numeros.append(int(palabra))
            else:
                # Números concatenados - separar
                numeros.extend(separar_numeros_ruleta(palabra))
    return numeros


def contar_seguidos_paridad(vector):
    contador_racha = 1
    i = 0
    for numero in vector[0:]:
        i+=1
        if numero != 0:
            paridad_actual = numero % 2  # Paridad del primer número
            break

    for numero in vector[i:]:
        if numero != 0:
            paridad = numero % 2
            if paridad == paridad_actual:
                contador_racha +=1
            else:
                break


    if contador_racha > UMBRAL_PARIDAD:
        if paridad_actual == 1:
            print(ESTILO_NEGRITA + COLOR_MORADO+"\nAPOSTA "+obtener_contrario(paridad_actual),COLOR_RESET+ESTILO_NEGRITA+" - RACHA PARIDAD!: ", contador_racha, COLOR_RESET)
        else:
            print(ESTILO_NEGRITA + COLOR_AMARILLO+"\nAPOSTA "+obtener_contrario(paridad_actual),COLOR_RESET+ESTILO_NEGRITA+" - RACHA PARIDAD!: ", contador_racha, COLOR_RESET)
    
        pygame.mixer.music.load("par.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
            break
    else:
        if paridad_actual==0:
            print(ESTILO_NEGRITA+"\nPAR: ", contador_racha, COLOR_RESET)
        else: 
            print(ESTILO_NEGRITA+"\nIMPAR: ", contador_racha, COLOR_RESET)



def contar_seguidos_mitades(vector):
    contador_racha = 1
    es_menor = vector[0] < 19
    i = 0
    for numero in vector[0:]:
        i+=1
        if numero != 0:
            if (numero < 19):
                es_menor = True
            else:
                es_menor = False
            break

    for numero in vector[i:]:
        if (numero < 19 and es_menor) or (numero >= 19 and not es_menor):
            if numero != 0:
                contador_racha +=1
        else:
            break

    if contador_racha > UMBRAL_MITADES:
        if es_menor:
            print(ESTILO_NEGRITA + COLOR_VERDE+"\nAPOSTA "+obtener_contrario_menor_mayor(es_menor),COLOR_RESET+ESTILO_NEGRITA+" - RACHA MITADES!: ", contador_racha, "\n"+COLOR_RESET)
        else:
            print(ESTILO_NEGRITA + COLOR_CYAN+"\nAPOSTA "+obtener_contrario_menor_mayor(es_menor),COLOR_RESET+ESTILO_NEGRITA+" - RACHA MITADES!: ", contador_racha, "\n"+COLOR_RESET)
        pygame.mixer.music.load("mayor.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
            break
    else:
        if es_menor:
            print(ESTILO_NEGRITA+"\nMITAD MENOR: ", contador_racha, "\n"+COLOR_RESET)
        else: 
            print(ESTILO_NEGRITA+"\nMITAD MAYOR: ", contador_racha, "\n"+COLOR_RESET)



def color_ruleta(numero):
    # Lista de números rojos en la ruleta
    rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

    # Si el número es 0 o no está en la lista de rojos, es negro; de lo contrario, es rojo
    if numero == 0:
        return "Verde"
    elif numero in rojos:
        return "Rojo"
    else:
        return "Negro"

def obtener_docena(numero):
    if numero == 0:
        return 0
    elif numero <= 12:
        return 1  # Primera docena
    elif numero <= 24:
        return 2  # Segunda docena
    else:
        return 3  # Tercera docena

def obtener_contrario_docena(docena_actual):
    if docena_actual == 1:
        return "2da o 3ra DOCENA"
    elif docena_actual == 2:
        return "1ra o 3ra DOCENA"
    else:
        return "1ra o 2da DOCENA"

def obtener_fila(numero):
    if numero == 0:
        return 0
    else:
        return ((numero - 1) % 3) + 1  # Retorna 1, 2 o 3

def obtener_contrario_fila(fila_actual):
    if fila_actual == 1:
        return "2da o 3ra FILA"
    elif fila_actual == 2:
        return "1ra o 3ra FILA"
    else:
        return "1ra o 2da FILA"

def contar_seguidos_color(vector):
    color_actual = color_ruleta(vector[0])
    contador_racha = 1

    for numero in vector[1:]:
        color = color_ruleta(numero)
        if color_actual == 'Verde':
            color_actual = color
        else:
            if color == color_actual:
                contador_racha += 1
            else:
                if numero != 0:
                    break

    if contador_racha > UMBRAL_COLORES:
        if color_actual == 'Negro':
            print(ESTILO_NEGRITA + COLOR_ROJO + "\nAPOSTA "+ "\033[4m"+obtener_contrario_color(color_actual)+"\033[0m" + COLOR_RESET +ESTILO_NEGRITA+ " - RACHA COLOR: " , contador_racha, COLOR_RESET)
        else:
            print(ESTILO_NEGRITA + COLOR_AZUL + "\nAPOSTA "+ "\033[4m"+obtener_contrario_color(color_actual)+"\033[0m" + COLOR_RESET +ESTILO_NEGRITA+" - RACHA COLOR: " , contador_racha,COLOR_RESET)
        pygame.mixer.music.load("win.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
            break 
    else:
         if color_actual=='Rojo':
            print(ESTILO_NEGRITA+"\nROJO: ", contador_racha,COLOR_RESET)
         else:
             if color_actual=='Negro':
                print(ESTILO_NEGRITA+"\nNEGRO: ", contador_racha,COLOR_RESET)


def contar_seguidos_docenas(vector):
    contador_racha = 1

    # Encontrar primer número no-cero para obtener docena inicial
    i = 0
    docena_actual = 0
    for numero in vector[0:]:
        i += 1
        if numero != 0:
            docena_actual = obtener_docena(numero)
            break

    # Contar números consecutivos en la misma docena
    for numero in vector[i:]:
        if numero != 0:
            docena = obtener_docena(numero)
            if docena == docena_actual:
                contador_racha += 1
            else:
                break

    # Mostrar separador de docenas
    print("--------docenas--------")

    # Mostrar alerta si supera el umbral
    if contador_racha > UMBRAL_DOCENAS:
        nombre_docena = ["", "1ra", "2da", "3ra"][docena_actual]
        print(ESTILO_NEGRITA + COLOR_VERDE + "\nAPOSTA " + obtener_contrario_docena(docena_actual) +
              COLOR_RESET + ESTILO_NEGRITA + " - RACHA " + nombre_docena + " DOCENA!: " + str(contador_racha) + COLOR_RESET)
        pygame.mixer.music.load("docenas.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
            break
    else:
        nombre_docena = ["", "1ra", "2da", "3ra"][docena_actual]
        print(ESTILO_NEGRITA + "\n" + nombre_docena + " DOCENA: ", contador_racha, COLOR_RESET)

    return contador_racha


def contar_seguidos_filas(vector):
    contador_racha = 1

    i = 0
    fila_actual = 0
    for numero in vector[0:]:
        i += 1
        if numero != 0:
            fila_actual = obtener_fila(numero)
            break

    for numero in vector[i:]:
        if numero != 0:
            fila = obtener_fila(numero)
            if fila == fila_actual:
                contador_racha += 1
            else:
                break

    print("\n--------filas--------")

    if contador_racha > UMBRAL_FILAS:
        nombre_fila = ["", "1ra", "2da", "3ra"][fila_actual]
        print(ESTILO_NEGRITA + COLOR_VERDE + "\nAPOSTA " + obtener_contrario_fila(fila_actual) +
              COLOR_RESET + ESTILO_NEGRITA + " - RACHA " + nombre_fila + " FILA!: " + str(contador_racha) + COLOR_RESET)
        pygame.mixer.music.load("filas.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
            break
    else:
        nombre_fila = ["", "1ra", "2da", "3ra"][fila_actual]
        print(ESTILO_NEGRITA + "\n" + nombre_fila + " FILA: ", contador_racha, COLOR_RESET)

    return contador_racha


def procesar():

    try:
        gausiano.redimensionar('temp_captura.png')

        results = reader.readtext(
            'imagen_redimensionada.png',
            allowlist='0123456789',
            text_threshold=0.5,
            low_text=0.4,
            width_ths=0.7
        )

        text = ''
        for x in results:
            text += x[1] + ' '

        # Limpiar separadores que EasyOCR puede confundir
        text = text.replace('/', ' ').replace('\\', ' ').replace('|', ' ')

        # Extraer números usando la nueva función que separa números concatenados
        vector_numeros = extraer_numeros_de_texto(text)

        if not vector_numeros:
            return

        os.system('cls')
        print("\n", vector_numeros)

        contar_seguidos_color(vector_numeros)
        contar_seguidos_paridad(vector_numeros)
        contar_seguidos_mitades(vector_numeros)
        contar_seguidos_docenas(vector_numeros)
        contar_seguidos_filas(vector_numeros)

    except Exception as e:
        print(f"Error al leer el texto en la imagen: {str(e)}")


# Inicializar reproductor de sonido (una sola vez)
pygame.mixer.init()
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

# Ciclo para capturar y analizar periódicamente
while True:
    captura = tomar_captura()
    grabar_captura(captura)
    procesar()
    time.sleep(intervalo_captura)
