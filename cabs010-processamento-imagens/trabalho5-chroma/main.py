import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Trabalho 5 de PDI - Chroma Key
# Autor: Marcos Rocha
# Implementação própria com base nos conceitos vistos em aula.


# Diretório e imagens disponíveis
image_dir = Path("img")
image_files = [
    "0.BMP",
    "1.bmp",
    "2.bmp",
    "3.bmp",
    "4.bmp",
    "5.bmp",
    "6.bmp",
    "7.bmp",
    "8.bmp"
]

# Processa cada imagem
for file in image_files:
    image_path = image_dir / file
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em {image_path}")
        return None, None
        
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)