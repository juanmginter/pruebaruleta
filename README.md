# Analizador de Patrones de Ruleta

Sistema automático de análisis de números de ruleta con detección de patrones estadísticos y alertas en tiempo real.

## Descripcion

Este proyecto captura números de ruleta en tiempo real mediante PaddleOCR (Reconocimiento Óptico de Caracteres), analiza patrones estadísticos y emite alertas sonoras cuando detecta rachas significativas.

## Funcionalidades Principales

- **Captura automática de pantalla** cada 4 segundos en una región específica (ROI)
- **Reconocimiento de números** mediante PaddleOCR
- **Detección de 3 tipos de patrones:**
  - Rachas de paridad (4+ números pares o impares consecutivos)
  - Rachas de mitades (4+ números bajos 1-18 o altos 19-36)
  - Rachas de color (4+ números rojos o negros consecutivos)
- **Alertas sonoras** cuando se detectan patrones
- **Recomendaciones de apuesta** basadas en el análisis

## Estructura del Proyecto

```
C:\pip\
├── prueba.py              # Script principal de análisis
├── gausiano.py            # Módulo de procesamiento de imágenes
├── capturas_prueba/       # Imágenes de prueba para calibración
├── par.wav                # Alerta racha par/impar
├── mayor.wav              # Alerta números mayores
├── win.wav                # Alerta racha de color
└── notificacion.wav       # Notificación genérica
```

## Requisitos

### Dependencias Python

```bash
pip install paddlepaddle paddleocr pyautogui pygame-ce opencv-python pillow numpy easygui matplotlib
```

> **Nota:** Se usa `pygame-ce` (Community Edition) en lugar de `pygame` por mejor compatibilidad.

### Dependencias del Sistema

- **Python 3.8 - 3.12** (PaddleOCR no soporta Python 3.13+)

## Uso

### Ejecución Principal

```bash
python prueba.py
```

### Configuración

Las constantes configurables en `prueba.py`:

```python
UMBRAL_MITADES = 4    # Mínimo para detectar racha de mitades
UMBRAL_COLORES = 4    # Mínimo para detectar racha de color
UMBRAL_PARIDAD = 4    # Mínimo para detectar racha par/impar
intervalo_captura = 4 # Segundos entre capturas
```

## Flujo de Procesamiento

```
1. CAPTURA
   └── pyautogui captura región de pantalla

2. PREPROCESAMIENTO
   └── Redimensionar → Mejorar contraste/brillo → Nitidez

3. OCR
   └── PaddleOCR extrae números (0-36)

4. ANÁLISIS DE PATRONES
   ├── contar_seguidos_color()     → Detecta rachas de color
   ├── contar_seguidos_paridad()   → Detecta rachas par/impar
   └── contar_seguidos_mitades()   → Detecta rachas de mitades

5. ALERTAS
   └── Sonido + mensaje en consola cuando racha > umbral
```

## Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `prueba.py` | Script principal que ejecuta el análisis en tiempo real |
| `gausiano.py` | Módulo de procesamiento: redimensiona a 970x90px, ajusta contraste (1.1x) y brillo (1.2x) |

## Tecnologías Utilizadas

- **PaddleOCR** - Reconocimiento óptico de caracteres
- **PyAutoGUI** - Captura de pantalla
- **Pygame** - Reproducción de sonidos
- **OpenCV** - Procesamiento de imágenes
- **Pillow** - Manipulación de imágenes
- **NumPy** - Operaciones numéricas
- **Colorama** - Colores en consola

## Notas

- El sistema está diseñado para Windows
- Ajustar las coordenadas ROI según la resolución de pantalla y posición de la aplicación de ruleta
- Los umbrales pueden modificarse según preferencias de detección
