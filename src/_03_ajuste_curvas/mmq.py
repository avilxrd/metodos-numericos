# Entrada:
# Dados tabelados;
# Função.

# Obter uma g(x) tal que f(x) ~= g(x)

# Problemas
# O que é uma boa aproximação?
# [x] 1. Erro total = 0. Erros podem se cancelar e dar um resultado enganoso.
# [x] 2. Erro total = 0, considerando módulo do erro local. A função módulo não é diferenciavel em 0.
# [v] 3. Considerar o erro total ao quadrado. Min ET^2.

# Como obter um g(x)?

# Erro Local: 
# E(xi) = f(xi) - g(xi), i=1, 2, ..., n

# Erro Total:
# "Soma dos erros locais"
# E(x1) + E(x2) + ... + E(xn)
# somatorio de [i=1, n] (E(xi))

import numpy as np
import matplotlib.pyplot as plt

from src.sistemas_lineares.eliminacao_gauss import gauss

"""
Recebe o grau de um polinômio e monta a matriz que 
será utilizada para os mínimos quadrados.
"""
def monta_matriz(grau: int, xi: list):
    if (grau < 1):
        return

    tamanho = grau + 1

    A = np.zeros((tamanho, tamanho))
    
    for i in range(tamanho):
        for j in range(tamanho):
            expoente = 2 * grau - i - j
            A[i, j] = np.sum(xi ** expoente)
    
    return A
   
"""
"""   
def monta_vetor(grau: int, xi:list, fxi: list):
    tamanho = grau + 1
    
    b = np.zeros(tamanho)
    
    for i in range(tamanho):
        expoente = grau - i
        b[i] = np.sum(fxi * (xi ** expoente))

    return b

"""
"""
def ajustar_curva(grau: int, xi: list, fxi: list):
    A = monta_matriz(grau, xi)
    b = monta_vetor(grau, xi, fxi)    
    coeficientes = gauss(A, b)
    plotar_ajuste(xi, fxi, coeficientes)
    return coeficientes

"""
"""
def plotar_ajuste(x, y, coeficientes):
    # Gera valores de X para desenhar a curva
    x_curva = np.linspace(min(x), max(x), 100)

    # Calcula os valores Y do polinômio
    y_curva = np.polyval(coeficientes, x_curva)

    # Pontos originais
    plt.scatter(x, y, label="Pontos tabelados")

    # Polinômio ajustado
    plt.plot(x_curva, y_curva, color="red", label="Polinômio MMQ")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Least Squares")
    plt.legend()
    plt.grid(True)

    plt.savefig("img/mmq.png", dpi=150, bbox_inches="tight")

def main():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 3, 5, 4, 6])
    
    grau = 2
    
    x = ajustar_curva(grau, x, y)
    
    return 0


if __name__ == "__main__":
    main()