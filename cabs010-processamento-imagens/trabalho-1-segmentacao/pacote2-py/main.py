#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.75
ALTURA_MIN = 10
LARGURA_MIN = 10
N_PIXELS_MIN = 20

#===============================================================================

def binariza (img, threshold):
    ''' Binarização simples por limiarização.
    
Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

    # TODO: escreva o código desta função.
    # Dica/desafio: usando a função np.where, dá para fazer a binarização muito
    # rapidamente, e com apenas uma linha de código!

    return np.where(img > threshold, 1.0, 0.0)

    # altura, largura, canais = img.shape
    # bin_img = img.copy()
    # for i in range(altura):
    #     for j in range(largura):
    #         for c in range(canais):
    #             if bin_img[i, j, c] > threshold:
    #                 bin_img[i, j, c] = 1.0
    #             else:
    #                 bin_img[i, j, c] = 0.0
    # return bin_img
#-------------------------------------------------------------------------------

def rotula (img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.

    altura, largura, _ = img.shape
    label = 0.1  # primeiro rótulo

    # Dicionário para guardar as posições de cada componente
    componentes_temp = {}


    # ---------------------------------------------------------
    # Primeira passada: rotulagem com flood fill recursivo
    # ---------------------------------------------------------

    def flood_fill(img, x0, y0, label):
        """
        Flood fill recursivo com vizinhança 4.
        
        Parâmetros:
        img: imagem binarizada (entrada e saída). Espera-se que pixels com valor 1.0
            sejam parte do objeto e que o valor rotulado seja um número como 0.1, 0.2, etc.
        x0, y0: coordenadas do pixel semente.
        label: valor do rótulo a ser atribuído aos pixels conectados.
        """
        altura, largura, _ = img.shape

        # Marca o pixel atual com o rótulo
        img[x0, y0, 0] = label

        # Vizinhança 4: cima, baixo, esquerda, direita
        vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in vizinhos:
            nx, ny = x0 + dx, y0 + dy

            # Verifica se está dentro da imagem
            if 0 <= nx < altura and 0 <= ny < largura:
                # Se ainda não rotulado (== 1.0), inunda recursivamente
                if img[nx, ny, 0] == 1.0:
                    flood_fill(img, nx, ny, label)



   
    for i in range(altura):
        for j in range(largura):
            if img[i, j, 0] == 1.0:  # encontrou uma nova semente
                flood_fill(img, i, j, label)  # aplica flood fill com rótulo atual
                label += 0.1  # incrementa para o próximo rótulo
    
    # ---------------------------------------------------------
    # Segunda passada: estatísticas por componente
    # ---------------------------------------------------------
    for i in range(altura):
        for j in range(largura):
            val = img[i, j, 0]
            if val >= 0.1:  # já foi rotulado
                if val not in componentes_temp:
                    componentes_temp[val] = {
                        'label': val,
                        'n_pixels': 0,
                        'T': i,
                        'B': i,
                        'L': j,
                        'R': j
                    }
                comp = componentes_temp[val]
                comp['n_pixels'] += 1
                comp['T'] = min(comp['T'], i)
                comp['B'] = max(comp['B'], i)
                comp['L'] = min(comp['L'], j)
                comp['R'] = max(comp['R'], j)


    # ---------------------------------------------------------
    # Filtro final e retorno
    # ---------------------------------------------------------
    componentes = []
    for comp in componentes_temp.values():
        altura_comp = comp['B'] - comp['T'] + 1
        largura_comp = comp['R'] - comp['L'] + 1
        if (comp['n_pixels'] >= n_pixels_min and
            altura_comp >= altura_min and
            largura_comp >= largura_min):
            componentes.append(comp)

    return componentes
#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
