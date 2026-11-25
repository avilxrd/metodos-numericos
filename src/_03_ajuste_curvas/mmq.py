# Entrada:
import numpy as np
import matplotlib.pyplot as plt

from src._02_sistemas_lineares.eliminacao_gauss import gauss

# Recebe o grau de um polinômio e monta a matriz do sistema 
# normal.
def monta_matriz(grau: int, xi):
    if (grau < 0):
        raise ValueError("Não é aceito grau negativo.")

    tamanho = grau + 1

    A = np.zeros((tamanho, tamanho))
    
    for i in range(tamanho):
        for j in range(tamanho):
            expoente = 2 * grau - i - j
            A[i, j] = np.sum(xi ** expoente)
    
    return A
   
# Monta o vetor dos termos independentes do sistema normal.
def monta_vetor(grau: int, xi, fxi):
    tamanho = grau + 1
    
    b = np.zeros(tamanho)
    
    for i in range(tamanho):
        expoente = grau - i
        b[i] = np.sum(fxi * (xi ** expoente))

    return b

# 
def ajustar_curva(grau: int, xi, fxi):
    xi = np.asarray(xi, dtype=float)
    fxi = np.asarray(fxi, dtype=float)

    if xi.ndim != 1 or fxi.ndim != 1:
        raise ValueError("xi e fxi devem ser vetores.")
    if xi.size == 0 or xi.size != fxi.size:
        raise ValueError("xi e fxi devem ter o mesmo tamanho não nulo.")
    if not np.isfinite(xi).all() or not np.isfinite(fxi).all():
        raise ValueError("Os dados devem ser finitos.")
    if grau < 0 or xi.size < grau + 1:
        raise ValueError("Grau incompatível com a quantidade de dados.")

    A = monta_matriz(grau, xi)
    b = monta_vetor(grau, xi, fxi)    
    coeficientes = gauss(A, b)
    plotar_ajuste(xi, fxi, coeficientes)
    return coeficientes

# 
def plotar_ajuste(x, y, coeficientes):
    fig, ax = plt.subplots()

    # Gera valores de X para desenhar a curva
    x_curva = np.linspace(min(x), max(x), 100)

    # Calcula os valores Y do polinômio
    y_curva = np.polyval(coeficientes, x_curva)

    # Pontos originais
    ax.scatter(x, y, label="Pontos tabelados")

    # Polinômio ajustado
    ax.plot(x_curva, y_curva, color="red", label="Polinômio MMQ")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Mínimos Quadrados")
    ax.legend()
    ax.grid(True)

    fig.savefig("img/mmq.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(fig)