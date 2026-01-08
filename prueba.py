import time
import easygui
import pyautogui
import easyocr
import pygame
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import gausiano
from PIL import Image, ImageEnhance, ImageFilter

# ===== CONSTANTES =====
UMBRAL_MITADES = 4
UMBRAL_COLORES = 4
UMBRAL_PARIDAD = 4

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
x = 1190  # Coordenada X del área de interés
y = 800  # Coordenada Y del área de interés
ancho = 350  # Ancho del área de interés
alto = 40  # Alto del área de interés


x = 1200  # Coordenada X del área de interés
y = 545  # Coordenada Y del área de interés
ancho = 310  # Ancho del área de interés
alto = 25 

x = 1125  # Coordenada X del área de interés
y = 255  # Coordenada Y del área de interés
ancho = 400  # Ancho del área de interés
alto = 30 

#plata actual
xacu = 264  # Coordenada X del área de interés
yacu = 981  # Coordenada Y del área de interés
anchoacu = 60  # Ancho del área de interés
altoacu = 30 


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
def tomar_captura_acu():
    captura = pyautogui.screenshot(region=(xacu, yacu, anchoacu, altoacu))
    return captura
# Función para analizar la captura de pantalla y tomar decisiones
def grabar_captura(captura):
    # Guardar la captura en un archivo temporal
    captura_guardada=captura.save("c:\\pip\\temp_captura.png")

    return captura_guardada

def grabar_acumulado(captura):
    # Guardar la captura en un archivo temporal
    captura_guardada=captura.save("c:\\pip\\temp_acumulado.png")

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
    # colores_rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    # if componente in colores_rojos:
    #     return "NEGRO"
    # else:
    #     return "ROJO"

    if componente == 'Rojo':
        return "NEGRO"
    else:
        return "ROJO"

#resultado_par_impar = obtener_contrario(componente)
#resultado_menor_mayor = obtener_contrario_menor_mayor(componente)
#resultado_color = obtener_contrario_color(componente)



def contar_seguidos_paridad(vector):
    
    #vector = [21, 21, 21, 21, 21, 21, 0, 21, 21, 22, 8, 29, 8, 19, 14, 36, 11]

    contador_racha = 1
    # umbral = 5  # Cambia esto según tus necesidades

    i=0
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
        # print("¡hay racha en paridad! ", contador_racha)
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
        # print("\nNo hay paridad considerable por el momento.")
        if paridad_actual==0:
            print(ESTILO_NEGRITA+"\nPAR: ", contador_racha, COLOR_RESET)
        else: 
            print(ESTILO_NEGRITA+"\nIMPAR: ", contador_racha, COLOR_RESET)



def contar_seguidos_mitades(vector):
    # conteo = 0
    # contador_racha = 0  # Contador para la racha de números seguidos
    contador_racha = 1 # Contador para la racha de números seguidos
    # umbral = 5  # Cambia esto según tus necesidades
    es_menor = vector[0] < 19 # Verifica si el primer número es menor

    i=0
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


    # # # for numero in vector:
    # # for numero in vector[1:]:
    # #     if (numero < 19 and es_menor) or (numero >= 19 and not es_menor):
    # #         if numero != 0:
    # #             contador_racha += 1  # Incrementa el contador de la racha
    # #     else:
    # #         break  # Detectó un cambio, termina el conteo


    # if conteo > umbral:
    if contador_racha > UMBRAL_MITADES:
        # print(ESTILO_NEGRITA + COLOR_DARKCYAN + "\nRACHA MITADES!: ", contador_racha, COLOR_RESET)
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
        # print(ESTILO_NEGRITA+"\nMitades: ", contador_racha, "\n"+COLOR_RESET)
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

# Tu vector de números
#vector_numeros = [29, 29, 29, 29, 29, 28, 8, 19, 14, 36, 11, 35]


    

def contar_seguidos_color(vector):
    
    # vector = [30, 0, 30, 0, 0, 30, 30, 30, 29, 8, 19, 14, 36, 11] 

    # Inicializar variables para el seguimiento
    color_actual = color_ruleta(vector[0])
    contador_racha = 1

    # umbral=5 

    # Recorrer el vector a partir del segundo elemento
    for numero in vector[1:]:
        color = color_ruleta(numero)
             
        # Si el color actual es igual al color actual del número, incrementar el contador
        if color_actual=='Verde':
                color_actual=color
        else: 
            if color == color_actual:
                contador_racha += 1
            else:
                if numero!=0: 
                    break
                       
            # Si el color cambia, termina el conteo
                           

    # Si encontramos más de 5 números seguidos del mismo color, marcarlo y reproducir un sonido
    if contador_racha > UMBRAL_COLORES:
        if color_actual == 'Negro':
            print(ESTILO_NEGRITA + COLOR_ROJO + "\nAPOSTA "+ "\033[4m"+obtener_contrario_color(color_actual)+"\033[0m" + COLOR_RESET +ESTILO_NEGRITA+ " - RACHA COLOR: " , contador_racha, COLOR_RESET)
        else:
            print(ESTILO_NEGRITA + COLOR_AZUL + "\nAPOSTA "+ "\033[4m"+obtener_contrario_color(color_actual)+"\033[0m" + COLOR_RESET +ESTILO_NEGRITA+" - RACHA COLOR: " , contador_racha,COLOR_RESET)
        # Reproducir un sonido de notificación (cambia la ruta al archivo de sonido que desees)
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
            



def procesar_acumulado():
    results = reader.readtext('temp_acumulado.png')
    text = ''
    for x in results:
        text += x[1] + ' '
    saldo_actual = float(text)
    print(saldo_actual)


#PROGRAMA PRINCIPAL                  
def procesar():

    try:
        gausiano.redimensionar('c:\\pip\\temp_captura.png')

        results = reader.readtext('imagen_redimensionada.png')

        text = ''
        for x in results:
            text += x[1] + ' '

        # Limpiar separadores que EasyOCR puede confundir
        text = text.replace('/', ' ').replace('\\', ' ').replace('|', ' ')

        numeros_texto = text.split()
        
        # fecha 04/10
        #Con este codigo, cuando captura cualquier cosa y le pone 11, cuenta como si hubiera una racha
        #Ademas de leer el 11 correctamente, sirve para avisar que se cerro sesion o que esta leyendo mal
        # Verificar si cada elemento es un número y, si no lo es (caso del 11 que lo toma como M1), transformar el elemento en el numero 11
        # for i in range(len(numeros_texto)):
        #     if not numeros_texto[i].isdigit():
        #         numeros_texto[i] = '11' 
        
        #Para leer el numero 11 correctamente
        if not numeros_texto[0].isdigit():
            numeros_texto[0] = '11'     

        # #Para leer el numero 11 correctamente
        # if not numeros_texto[0].isdigit() and numeros_texto[0] == 'M1':
        #     numeros_texto[0] = '11'     

        # Convertir los números de texto a enteros y almacenarlos en un vector
        vector_numeros = [int(numero) for numero in numeros_texto]
        # vector_numeros = [29, 36, 15, 26, 32, 28, 8, 19, 14, 36, 11, 35]
        # Imprimir el vector resultante
     
        if vector_numeros[0]>=70:
            vector_numeros[0]-=60
        os.system('cls')
        print("\n",vector_numeros)
        #return vector_numeros
        
        # Reproductor de sonido
        pygame.mixer.init()
        # Inicializar el reproductor de sonido
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

        # vector_numeros = [2, 4, 6, 8, 10, 12, 8, 19, 14, 36, 11, 35]
        # vector_numeros = [1, 3, 5, 7, 9, 11, 8, 19, 14, 36, 11, 35]

        # LLamada a las funciones que cuentan el color, la paridad y las mitades
        contar_seguidos_color(vector_numeros)
        contar_seguidos_paridad(vector_numeros)
        contar_seguidos_mitades(vector_numeros)
                
    except Exception as e:
        # Manejo de errores: aquí puedes especificar qué hacer si ocurre un error al leer el texto
        print(f"Error al leer el texto en la imagen: {str(e)}")
    



# Ciclo para capturar y analizar periódicamente
while True:
    #os.system('cls')
    vector_numeros=[]
   # captura = tomar_captura()
   # captura_guardada=grabar_captura(captura)
    #acumulado= tomar_captura_acu()
    #acumulado_guardado=grabar_acumulado(acumulado)

    
    # Faltan agregar todos los umbrales de rachas aca y pasarselos a la funcion procesar.
    # O Ponerlos como constantes.
    #procesar_acumulado()
    procesar()

    time.sleep(intervalo_captura)
