# Analizador de Patrones de Ruleta

Sistema automático de análisis de números de ruleta con detección de patrones estadísticos y alertas en tiempo real.

## Descripcion

Este proyecto captura números de ruleta en tiempo real mediante EasyOCR (Reconocimiento Óptico de Caracteres), analiza patrones estadísticos y emite alertas sonoras cuando detecta rachas significativas.

## Funcionalidades Principales

- **Captura automática de pantalla** cada 4 segundos en una región específica (ROI)
- **Reconocimiento de números** mediante EasyOCR
- **Detección de 5 tipos de patrones:**
  - Rachas de paridad (4+ números pares o impares consecutivos)
  - Rachas de mitades (4+ números bajos 1-18 o altos 19-36)
  - Rachas de color (4+ números rojos o negros consecutivos)
  - Rachas de docenas (4+ números en la misma docena: 1-12, 13-24, 25-36)
  - Rachas de filas (4+ números en la misma fila del tablero)
- **Alertas sonoras** cuando se detectan patrones
- **Recomendaciones de apuesta** basadas en el análisis

## Estructura del Proyecto

```
C:\ruleta\
├── ruleta_ejecutable.py   # Script principal de análisis
├── gausiano.py            # Módulo de procesamiento de imágenes
├── requirements.txt       # Dependencias del proyecto
├── par.wav                # Alerta racha par/impar
├── mayor.wav              # Alerta números mayores/menores
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
pip install pyautogui easyocr pygame-ce opencv-python
```

> **Nota:** Se usa `pygame-ce` (Community Edition) en lugar de `pygame` por mejor compatibilidad.

### Dependencias del Sistema

- **Python 3.8 - 3.12**

## Uso

### Ejecución Principal

```bash
python ruleta_ejecutable.py
```

### Configuración

Las constantes configurables en `ruleta_ejecutable.py`:

```python
UMBRAL_MITADES = 4    # Mínimo para detectar racha de mitades
UMBRAL_COLORES = 4    # Mínimo para detectar racha de color
UMBRAL_PARIDAD = 4    # Mínimo para detectar racha par/impar
UMBRAL_DOCENAS = 4    # Mínimo para detectar racha de docenas
UMBRAL_FILAS = 4      # Mínimo para detectar racha de filas
intervalo_captura = 4 # Segundos entre capturas
```

## Flujo de Procesamiento

```
1. CAPTURA
   └── pyautogui captura región de pantalla

2. PREPROCESAMIENTO (OpenCV)
   └── Escalado 4x → Desenfoque ligero → Mantener color

3. OCR
   └── EasyOCR extrae números → separar_numeros_ruleta() separa números concatenados

4. ANÁLISIS DE PATRONES
   ├── contar_seguidos_color()     → Detecta rachas de color
   ├── contar_seguidos_paridad()   → Detecta rachas par/impar
   ├── contar_seguidos_mitades()   → Detecta rachas de mitades
   ├── contar_seguidos_docenas()   → Detecta rachas de docenas
   └── contar_seguidos_filas()     → Detecta rachas de filas

5. ALERTAS
   └── Sonido + mensaje en consola cuando racha > umbral
```

## Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `ruleta_ejecutable.py` | Script principal que ejecuta el análisis en tiempo real |
| `gausiano.py` | Módulo de procesamiento con OpenCV: escalado 4x, desenfoque ligero, mantiene color |
| `requirements.txt` | Lista de dependencias Python del proyecto |

## Distribución de Números

### Docenas
- **1ra Docena:** 1-12
- **2da Docena:** 13-24
- **3ra Docena:** 25-36

### Filas
- **1ra Fila:** 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
- **2da Fila:** 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35
- **3ra Fila:** 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36

## Tecnologías Utilizadas

- **EasyOCR** - Reconocimiento óptico de caracteres
- **PyAutoGUI** - Captura de pantalla
- **Pygame-CE** - Reproducción de sonidos
- **OpenCV** - Preprocesamiento de imágenes (escalado, desenfoque)

## Hallazgos de Investigacion OCR

Durante el desarrollo se investigaron las mejores practicas para optimizar EasyOCR en deteccion de numeros. Segun la documentacion oficial y issues de GitHub:

1. **EasyOCR funciona MEJOR con imagenes a color** - no convertir a escala de grises
2. **Umbralizacion binaria inversa** (`THRESH_BINARY_INV`) mejora deteccion de numeros
3. **Escalado + desenfoque** (`cv2.blur(img, (3,3))`) es la combinacion mas efectiva
4. **Parametro `text_threshold=0.3`** mejora deteccion de numeros pequenos
5. **Tamano minimo**: imagenes deben tener >300 PPI para buen rendimiento
6. **Numeros concatenados**: EasyOCR puede juntar numeros cercanos, se implemento `separar_numeros_ruleta()` para separarlos

**Fuentes:**
- [EasyOCR Issue #341 - Numeros individuales](https://github.com/JaidedAI/EasyOCR/issues/341)
- [EasyOCR Issue #407 - Solo numeros](https://github.com/JaidedAI/EasyOCR/issues/407)
- [PyImageSearch - Preprocessing for OCR](https://pyimagesearch.com/2021/11/22/improving-ocr-results-with-basic-image-processing/)

## Notas

- El sistema esta disenado para Windows
- Ajustar las coordenadas ROI segun la resolucion de pantalla y posicion de la aplicacion de ruleta
- Los umbrales pueden modificarse segun preferencias de deteccion
