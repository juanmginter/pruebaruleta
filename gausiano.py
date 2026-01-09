import cv2
import numpy as np
import os

# Inicializar Super Resolution con EDSR (mejor calidad)
sr = cv2.dnn_superres.DnnSuperResImpl_create()
modelo_path = os.path.join(os.path.dirname(__file__), "EDSR_x4.pb")
sr.readModel(modelo_path)
sr.setModel("edsr", 4)

def redimensionar(captura):
    imagen = cv2.imread(captura)

    # Super Resolution con EDSR
    imagen = sr.upsample(imagen)

    # Unsharp mask ligero para mejorar enfoque
    gaussian = cv2.GaussianBlur(imagen, (0, 0), 1.0)
    imagen = cv2.addWeighted(imagen, 1.3, gaussian, -0.3, 0)

    cv2.imwrite('imagen_redimensionada.png', imagen)
