import cv2
import os
import numpy as np
import sys
from blur_algorithms import blur_ingenuo, blur_separavel, blur_integral


# Trabalho de PDI - Filtro da Média (Ingênuo, Separável e Integral)
# Autor: Marcos Rocha
# Implementação própria com base nos conceitos vistos em aula.


IMAGEM_DIR = "imagens"

ALGORITMOS = {
    "ingueno": blur_ingenuo,
    "separavel": blur_separavel,
    "integral": blur_integral
}


IMAGENS = ["a01 - Original.bmp", "b01 - Original.bmp"]

CASOS_TESTE = [
    ("a01 - Original.bmp", "a02 - Borrada 3x3.bmp", (3, 3), "ingueno"),
    ("a01 - Original.bmp", "a03 - Borrada 3x13.bmp", (3, 13), "ingueno"),
    ("a01 - Original.bmp", "a04 - Borrada 11x1.bmp", (11, 1), "separavel"),
    ("a01 - Original.bmp", "a05 - Borrada 51x21.bmp", (51, 21), "integral"),
    ("b01 - Original.bmp", "b02 - Borrada 7x7.bmp", (7, 7), "ingueno"),
    ("b01 - Original.bmp", "b03 - Borrada 11x15.bmp", (11, 15), "integral"),
]

def comparar(imagem1, imagem2):
    diff = cv2.absdiff(imagem1, imagem2)
    return np.max(diff)


def testar_algoritmo(nome_alg, funcao, imagem, nome_arquivo, ksize):
    print(f"Testando: {nome_alg} com {nome_arquivo} | Kernel: {ksize}")
    resultado = funcao(imagem, ksize)
    
    opencv_blur = cv2.blur(imagem, (ksize))
   
    max_diff = comparar(resultado, opencv_blur)

    if max_diff == 0:
        print(f"{nome_alg}: Resultado idêntico. ")
    else:
        print(f"{nome_alg}: diferenças detectadas (máx: {max_diff})")

def main():
    print("=== Filtro de Média - Execução de Testes Automáticos ===")

    tamanhos_kernel = [
        (3, 3),
        (3 , 5), 
        (5, 11), 
         (3, 21),
         (19, 3),
         (11, 11),
        
        ]
    algoritmos = [
        ("blur_ingenuo", blur_ingenuo),
        ("separavel", blur_separavel),
        ("integral", blur_integral)
    ]

    for nome_imagem in IMAGENS:
        caminho = os.path.join(IMAGEM_DIR, nome_imagem)
        imagem = cv2.imread(caminho)
        if imagem is None:
            print(f"Erro ao ler {nome_imagem}, ignorando.")
            continue

        for k in tamanhos_kernel:
            print(f"\n--- Imagem: {nome_imagem} | Kernel: {k} ---")
            for nome_alg, funcao in algoritmos:
                testar_algoritmo(nome_alg, funcao, imagem, nome_imagem, k)



    # print("\n=== Exibindo Comparações Visuais ===")
    # exemplo_imagem = os.path.join(IMAGEM_DIR, IMAGENS[1])
    # imagem = cv2.imread(exemplo_imagem)

    # for nome_alg, funcao in algoritmos:
    #     resultado = funcao(imagem, 5)
    #     cv2.imshow(f"Original - {nome_alg}", imagem)
    #     cv2.imshow(f"Resultado - {nome_alg}", resultado)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()



def main_alternativo():
    print("====== Teste de filtro da media ======\n")
    resultados = []

    for original_nome, borrada_nome, ksize in CASOS_TESTE:
        original_path = os.path.join(IMAGEM_DIR, original_nome)
        borrada_path = os.path.join(IMAGEM_DIR, borrada_nome)

        original = cv2.imread(original_path)
        borrada = cv2.imread(borrada_path)

        if original is None or borrada is None:
            print(f"Erro ao carregar: {original_nome} ou {borrada_nome}")
            continue

        for nome_alg, func in ALGORITMOS.items():
            print(f"--> Testando {nome_alg:<9} | Kernel: {ksize} | {borrada_nome}")
            try:
                saida = func(original, ksize)
                diff_nome = f"diff_{nome_alg}_{borrada_nome.replace(' ', '_')}"
                max_diff = comparar(saida, borrada)

                resultados.append((borrada_nome, nome_alg, ksize, max_diff))

                if max_diff == 0:
                    print("- Resultado identico.")
                else:
                    print(f"!!!! Diferenca detectada. Max: {max_diff} -> {diff_nome}")
            except Exception as e:
                print(f"Erro ao processar {borrada_nome} com {nome_alg}: {e}")

    print("\n====== Resumo dos testes ======")
    for nome, alg, k, diff in resultados:
        print(f"{nome:<30} | {alg:<9} | kernel={k} | diferença={diff}")


if __name__ == "__main__":
    main()
    # main_alternativo()
