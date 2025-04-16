# 🧪 Trabalho 2 — Filtros de Média (Blur)

**Disciplina:** Processamento Digital de Imagens (CABS010)  
**Professor:** Bogdan Tomoyuki Nassu  
**Aluno:** Marcos  
**Data de Entrega:** 6 de maio  
**Peso:** 1.6 (de 10)

---

## 🎯 Objetivo

Implementar três algoritmos para o **filtro da média (blur)**:

1. **Algoritmo Ingênuo**  
2. **Filtro Separável** (com ou sem uso de somas anteriores)  
3. **Filtro com Imagens Integrais**

---

## 🛠️ Instruções

- Todas as três implementações devem estar no **mesmo arquivo** (ex: `blur.c`).
- Um programa principal (`main.c`) deve permitir testar as três versões.
- Para imagens **coloridas**, processe cada canal **RGB** independentemente.
- **Margens:**
  - Integral: considerar apenas pixels válidos.
  - Ingênuo e separável: pode ignorar janelas fora da imagem.

---

## 🧪 Comparações

Se estiver utilizando OpenCV, compare os resultados com a função `cv::blur`, exceto nas margens (diferenças esperadas).

---

## 📂 Estrutura dos Arquivos

- `main.c`: Interface principal para executar e comparar os filtros.
- `blur.c`: Implementações dos três algoritmos.
- `blur.h`: Declarações de funções e structs auxiliares.
- `imagens/`: Contém imagens fornecidas para testes.

---

## ✅ Status

- [x] Estrutura organizada
- [ ] Implementação do algoritmo ingênuo
- [ ] Implementação do filtro separável
- [ ] Implementação com imagem integral
- [ ] Testes com imagens coloridas
- [ ] Comparação com OpenCV (opcional)

---

## 📦 Compilação (exemplo)

```bash
gcc main.c blur.c -o trabalho_blur
