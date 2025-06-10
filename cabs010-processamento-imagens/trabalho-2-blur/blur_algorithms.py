import numpy as np
import cv2

def blur_ingenuo(image, ksize):
    """
    Filtro da média 'ingênuo' (direto), com bordas tratadas usando
    reflexão tipo BORDER_REFLECT_101 
    """
    
    if isinstance(ksize, int):
        kw = kh = ksize
    else:
        kw, kh = ksize

    h, w = image.shape[:2]
    pad_y = kh // 2
    pad_x = kw // 2

    # Garante 3 dimensões
    if len(image.shape) == 2:
        image = np.expand_dims(image, axis=-1)

    channels = image.shape[2]
     
    output = np.zeros_like(image, dtype=np.uint8)


    for c in range(channels):
        for y in range(h):
            for x in range(w):
                soma = 0.0
                for j in range(-pad_y, pad_y + 1):
                    for i in range(-pad_x, pad_x + 1):
                        yy = y + j
                        xx = x + i

                        # # Reflexão tipo BORDER_REFLECT_101
                        yy = abs(yy) if yy < 0 else (2 * h - yy - 2 if yy >= h else yy)
                        xx = abs(xx) if xx < 0 else (2 * w - xx - 2 if xx >= w else xx)
                    
                        soma += image[yy, xx, c]

                output[y, x, c] = np.round(soma / (kh * kw))

    # Remove dimensão extra se for imagem cinza 
    if output.shape[2] == 1:
        return output[:, :, 0]
    
    return output

def blur_separavel(image, ksize):
    """
    Filtro da média separável
    Reutilizei o resultado do passo anterior, o que pode ter introduzido pequenas 
    diferenças devido ao arredondamento acumulado na etapa anterior.
    """
    if isinstance(ksize, int):
        kw = kh = ksize
    else:
        kw, kh = ksize

    resultado_horizontal = blur_ingenuo(image, (kw, 1))

    resultado_final = blur_ingenuo(resultado_horizontal, (1, kh))

    return resultado_final

def blur_integral(image, ksize):
    """
    Filtro da média utilizando imagem integral
    Neste ele não da igual o cv2, acredito que a borda é tratada de forma diferente
    """

    if isinstance(ksize, int):
        kw = kh = ksize
    else:
        kw, kh = ksize

    h, w = image.shape[:2]
    pad_y = kh // 2
    pad_x = kw // 2

    # Garante 3 dimensões
    if len(image.shape) == 2:
        image = np.expand_dims(image, axis=-1)

    channels = image.shape[2]

    # Converter para float32 para evitar overflow nas somas
    image = image.astype(np.float32)
    integral = np.zeros_like(image, dtype=np.float32)

    #Soma incremental pela vertical
    for x in range(w):
        for ch in range(channels):
            soma = 0.0
            for y in range(h):
                soma += image[y, x, ch]
                integral[y, x, ch] = soma

    #soma incremental pela horizontal
    for y in range(h):
        for ch in range(channels):
            soma = 0.0
            for x in range(w):
                soma += integral[y, x, ch]
                integral[y, x, ch] = soma



    output = np.zeros_like(image, dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            y1 = max(0, y - pad_y)
            y2 = min(h - 1, y + pad_y)
            x1 = max(0, x - pad_x)
            x2 = min(w - 1, x + pad_x)

            area = (y2 - y1 + 1) * (x2 - x1 + 1)

            for ch in range(channels):
                A = integral[y2, x2, ch]
                B = integral[y1 - 1, x2, ch] if y1 > 0 else 0
                C = integral[y2, x1 - 1, ch] if x1 > 0 else 0
                D = integral[y1 - 1, x1 - 1, ch] if y1 > 0 and x1 > 0 else 0

                soma = A - B - C + D
                output[y, x, ch] = np.round(soma / area)

    # Remove dimensão extra se for imagem cinza 
    if output.shape[2] == 1:
        return output[:, :, 0]
    
    return output
