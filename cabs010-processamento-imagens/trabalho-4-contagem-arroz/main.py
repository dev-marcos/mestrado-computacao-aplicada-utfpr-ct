import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Trabalho 4 de PDI - Contagem de Arroz
# Autor: Marcos Rocha
# Implementação própria com base nos conceitos vistos em aula.

# Diretório e imagens disponíveis
image_dir = Path("trabalho4")
image_files = [
    "60.bmp",
    "82.bmp",
    "114.bmp",
    "150.bmp",
    "205.bmp"
]

# Com matplotlib eu consigo visualizar melhor a imagem
def show_image(title, img):
    plt.figure()
    plt.title(title)
    cmap = 'gray' if len(img.shape) == 2 else None
    plt.imshow(img, cmap=cmap)
    plt.axis('off')
    plt.show(block=False) 


# Processa cada imagem
for file in image_files:
    img_path = image_dir / file
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Erro ao carregar {file}")
        continue

    # Etapa 1: blur para estimar o fundo

    ksize= 255

    blurred = cv2.GaussianBlur(img, (ksize, ksize), 0)
    #show_image("Imagem borrada, blurred)

    # Etapa 2: diferença entre original e borrada
    diff = cv2.absdiff(img, blurred)
    # show_image("Diferença", diff)


    # Etapa 2.5: Realce de bordas antes do Otsu
    # Essa etapa é adicionada para melhorar a separação entre os grãos de arroz,
    # especialmente nos casos em que eles estão muito próximos ou colados.

    edges = cv2.Canny(cv2.GaussianBlur(diff, (3, 3), 0), 50, 150)
    # show_image("edges", edges)

    # Subtrai as bordas dilatadas da imagem de diferença para acentuar divisões
    realce = cv2.subtract(diff, edges)
    # show_image("Realce com bordas - antes do Otsu", realce)
    
    # Etapa 3: Otsu
    _, binary = cv2.threshold(realce, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # show_image(f'Binarizada com Otsu {file}', binary)

    # Etapa 4: remoção de ruído com operação de abertura
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    limpa = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    # show_image("Após Abertura (remoção de ruído)", limpa)
     
    # Etapa 5: segmentação com connectedComponents, não queria usar o minha implementacao de flood_fill
    num_labels, labels = cv2.connectedComponents(limpa)

    # Etapa 6: obter áreas dos componentes
    areas = [(labels == i).sum() for i in range(1, num_labels)]


    # Etapa 7: remoção de outliers com método IQR
    componentes = np.array(areas)

    Q1 = np.percentile(componentes, 25)
    Q3 = np.percentile(componentes, 75)
    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    # Mantém apenas valores dentro do intervalo interquartil
    componentes_filtrados = componentes[(componentes >= limite_inferior) & (componentes <= limite_superior)]

    # Notei que com median o resultado é melhor que mean
    tamanho_medio = np.median(componentes_filtrados)


    # Etapa 8: contagem final ajustada
    contagem_final = 0

    # Separei apenas, pois queria testar umas tecnicas para tentar reajustar a borda 
    # somente de cada compoente grande para identificar a quantidade sem fazer a divisao
    componentes_validos = []
    componentes_grandes = [] 


    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


    for label, area in enumerate(areas):
        if area < 0.2 * tamanho_medio:
            continue  #ruido

        mask = (labels == label + 1).astype(np.uint8)
        x, y, w, h = cv2.boundingRect(mask)

        if area < 1.5 * tamanho_medio:
            componentes_validos.append(area)
            contagem_final += 1
            cor = (0, 255, 0) #green


        else:
            componentes_grandes.append(((label + 1), area))
            estimado = round(area / tamanho_medio)
            contagem_final += estimado
            cor = (0, 0, 255) #blue
            cv2.putText(img_color, str(estimado), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, cor, 1, cv2.LINE_AA)
        
        cv2.rectangle(img_color, (x, y), (x + w, y + h), cor, 1)

    
    show_image("Graos detectados com bounding boxes", img_color)

    # print("Componentes validos (1 grao):", len(componentes_validos))
    # print("Componentes grandes (mais de 1 grao):", len(componentes_grandes))
    print(f'{file} - Contagem final estimada de graos:', contagem_final)
    

    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()