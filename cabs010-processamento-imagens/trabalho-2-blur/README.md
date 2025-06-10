# 🧪 Trabalho 2 — Filtros de Média (Blur) — Python

**Disciplina:** Processamento Digital de Imagens (CABS010)  
**Professor:** Bogdan Tomoyuki Nassu  
**Aluno:** Marcos  
**Data de Entrega:** 6 de maio  
**Peso:** 1.6 (de 10)

---

## 🎯 Objetivo

Implementar três algoritmos para o **filtro da média (blur)** em Python:

1. **Algoritmo Ingênuo**  
2. **Filtro Separável** (com ou sem uso de somas anteriores)  
3. **Filtro com Imagens Integrais**

---

## 📦 Estrutura dos Arquivos

- `main.py`: Interface principal do programa. Permite executar e comparar os três métodos.
- `blur_algorithms.py`: Contém as implementações dos filtros.
- `imagens/`: Imagens de teste fornecidas no pacote.

---

## 🧪 Regras e Observações

- Para imagens **coloridas**, cada canal **R, G e B** deve ser processado separadamente.
- **Tratamento das bordas:**
  - **Imagens integrais:** média com apenas pixels válidos.
  - **Demais:** pode ignorar regiões fora da imagem.

- Se usar OpenCV, compare com `cv2.blur()` (resultados devem ser semelhantes, exceto nas bordas).

---

## ▶️ Como executar

### 1. Instalar dependências

```bash
pip install numpy opencv-python
