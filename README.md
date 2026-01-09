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
pip install pyautogui easyocr pygame-ce pillow
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

2. PREPROCESAMIENTO
   └── Redimensionar → Mejorar contraste/brillo → Nitidez

3. OCR
   └── EasyOCR extrae números → corregir_numero_ocr() corrige errores (ej: 719→19)

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
| `gausiano.py` | Módulo de procesamiento: redimensiona a 970x90px, ajusta contraste (1.1x) y brillo (1.2x) |
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
- **Pillow** - Manipulación y preprocesamiento de imágenes

## Notas

- El sistema está diseñado para Windows
- Ajustar las coordenadas ROI según la resolución de pantalla y posición de la aplicación de ruleta
- Los umbrales pueden modificarse según preferencias de detección
