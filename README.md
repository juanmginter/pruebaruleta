# Analizador de Patrones de Ruleta

Sistema automatico de analisis de numeros de ruleta con deteccion de patrones estadisticos y alertas en tiempo real.

## Descripcion

Este proyecto captura numeros de ruleta en tiempo real mediante EasyOCR (Reconocimiento Optico de Caracteres), analiza patrones estadisticos y emite alertas sonoras cuando detecta rachas significativas.

## Funcionalidades Principales

- **Captura automatica de pantalla** cada 4 segundos en una region especifica (ROI)
- **Reconocimiento de numeros** mediante EasyOCR
- **Super Resolution con Deep Learning** para mejorar calidad de imagen (modelo EDSR)
- **Deteccion de 5 tipos de patrones:**
  - Rachas de paridad (4+ numeros pares o impares consecutivos)
  - Rachas de mitades (4+ numeros bajos 1-18 o altos 19-36)
  - Rachas de color (4+ numeros rojos o negros consecutivos)
  - Rachas de docenas (4+ numeros en la misma docena: 1-12, 13-24, 25-36)
  - Rachas de filas (4+ numeros en la misma fila del tablero)
- **Alertas sonoras** cuando se detectan patrones
- **Recomendaciones de apuesta** basadas en el analisis

## Estructura del Proyecto

```
C:\ruleta\
├── ruleta_ejecutable.py   # Script principal de analisis
├── gausiano.py            # Modulo de procesamiento de imagenes con Super Resolution
├── EDSR_x4.pb             # Modelo de Super Resolution (Deep Learning)
├── requirements.txt       # Dependencias del proyecto
├── par.wav                # Alerta racha par/impar
├── mayor.wav              # Alerta numeros mayores/menores
├── win.wav                # Alerta racha de color
├── docenas.wav            # Alerta racha de docenas
└── filas.wav              # Alerta racha de filas
```

## Requisitos

### Dependencias Python

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install pyautogui easyocr pygame-ce opencv-contrib-python==4.9.0.80 "numpy<2"
```

> **Nota:** Se requiere `opencv-contrib-python` (no `opencv-python`) para Super Resolution.
> **Nota:** Se usa `pygame-ce` (Community Edition) en lugar de `pygame` por mejor compatibilidad.

### Dependencias del Sistema

- **Python 3.12** (requerido para compatibilidad con Super Resolution)

### Modelo de Super Resolution

El modelo EDSR_x4.pb se descarga automaticamente o manualmente desde:
```bash
curl -L -o EDSR_x4.pb "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x4.pb"
```

## Uso

### Ejecucion Principal

```bash
py -3.12 ruleta_ejecutable.py
```

### Configuracion

Las constantes configurables en `ruleta_ejecutable.py`:

```python
UMBRAL_MITADES = 4    # Minimo para detectar racha de mitades
UMBRAL_COLORES = 4    # Minimo para detectar racha de color
UMBRAL_PARIDAD = 4    # Minimo para detectar racha par/impar
UMBRAL_DOCENAS = 4    # Minimo para detectar racha de docenas
UMBRAL_FILAS = 4      # Minimo para detectar racha de filas
intervalo_captura = 4 # Segundos entre capturas
```

## Flujo de Procesamiento

```
1. CAPTURA
   └── pyautogui captura region de pantalla

2. PREPROCESAMIENTO (OpenCV + Deep Learning)
   ├── Super Resolution EDSR 4x (mejora calidad sin blur)
   └── Unsharp Mask ligero (mejora enfoque)

3. OCR
   ├── EasyOCR extrae numeros (width_ths=0.3, paragraph=False)
   └── Procesamiento individual de cada deteccion (evita fusion de numeros)

4. ANALISIS DE PATRONES
   ├── contar_seguidos_color()     → Detecta rachas de color
   ├── contar_seguidos_paridad()   → Detecta rachas par/impar
   ├── contar_seguidos_mitades()   → Detecta rachas de mitades
   ├── contar_seguidos_docenas()   → Detecta rachas de docenas
   └── contar_seguidos_filas()     → Detecta rachas de filas

5. ALERTAS
   └── Sonido + mensaje en consola cuando racha > umbral
```

## Archivos del Proyecto

| Archivo | Descripcion |
|---------|-------------|
| `ruleta_ejecutable.py` | Script principal que ejecuta el analisis en tiempo real |
| `gausiano.py` | Modulo de procesamiento: Super Resolution EDSR 4x + Unsharp Mask |
| `EDSR_x4.pb` | Modelo de red neuronal para Super Resolution |
| `requirements.txt` | Lista de dependencias Python del proyecto |

## Distribucion de Numeros

### Docenas
- **1ra Docena:** 1-12
- **2da Docena:** 13-24
- **3ra Docena:** 25-36

### Filas
- **1ra Fila:** 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
- **2da Fila:** 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35
- **3ra Fila:** 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36

## Tecnologias Utilizadas

- **EasyOCR** - Reconocimiento optico de caracteres
- **PyAutoGUI** - Captura de pantalla
- **Pygame-CE** - Reproduccion de sonidos
- **OpenCV DNN Super Resolution** - Ampliacion de imagen con Deep Learning (EDSR)

## Hallazgos de Investigacion OCR

Durante el desarrollo se investigaron las mejores practicas para optimizar la deteccion de numeros:

### Super Resolution vs Interpolacion Tradicional
1. **EDSR** (Enhanced Deep Super Resolution) produce imagenes mas nitidas que interpolacion tradicional
2. **INTER_LANCZOS4** es la mejor interpolacion tradicional pero inferior a Deep Learning
3. **FSRCNN/ESPCN** son mas rapidos pero menos precisos que EDSR

### Preprocesamiento
1. **EasyOCR funciona MEJOR con imagenes a color** - no convertir a escala de grises
2. **Unsharp Mask** mejora enfoque sin agregar ruido
3. **Evitar blur excesivo** - difumina los bordes de los numeros

### Parametros EasyOCR
1. **text_threshold=0.5** reduce falsos positivos
2. **width_ths=0.3** evita fusion de numeros cercanos (menor = mas estricto)
3. **paragraph=False** mantiene cada deteccion separada
4. **allowlist='0123456789'** restringe a solo digitos
5. **Procesamiento individual** de cada deteccion para evitar concatenacion incorrecta

**Fuentes:**
- [OpenCV DNN Super Resolution](https://docs.opencv.org/4.x/d5/d29/tutorial_dnn_superres_upscale_image_single.html)
- [EDSR Paper](https://arxiv.org/abs/1707.02921)
- [EasyOCR Documentation](https://www.jaided.ai/easyocr/documentation/)

## Notas

- El sistema esta disenado para Windows
- **Requiere Python 3.12** para compatibilidad con opencv-contrib-python y numpy
- Ajustar las coordenadas ROI segun la resolucion de pantalla y posicion de la aplicacion de ruleta
- Los umbrales pueden modificarse segun preferencias de deteccion
