import numpy as np
from matplotlib import pyplot as plt

from src._02_sistemas_lineares.eliminacao_gauss import gauss

# Recebe uma lista de pontos x (x1, x2, ..., xn). Cria a matriz
# de potências. Retorna a matriz de potências.
def montar_matriz(x: list[float]) -> np.ndarray:
    n = len(x)
    V = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            V[i, j] = x[i] ** j

    return V

# Plota informações interessantes para o usuário.
def plotar_ajuste(x, y, coeficientes):
    fig, ax = plt.subplots()
    x_curva = np.linspace(min(x), max(x), 100)
    y_curva = np.polyval(coeficientes[::-1], x_curva)
    ax.plot(x_curva, y_curva, color="red", label="Interpolação por definição")

    ax.scatter(x, y, label="Pontos tabelados")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Interpolação por Definição")
    ax.legend()
    ax.grid(True)

    fig.savefig("img/interpol_def.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(fig)

# Interface para rodar o algorítmo completo.
# Monta a matriz, calcula os coeficientes
# utilizando o método de Gauss implementado.
def definicao(x, y):
    if len(np.unique(x)) != len(x):
        raise ValueError("Os valores de x devem ser distintos.")

    V = montar_matriz(x)
    coeficientes = gauss(V, y)
    plotar_ajuste(x, y, coeficientes)
    
    return coeficientes

# Interface de teste.
def main():
    x = [-1, 0, 1, 2]
    y = [0, 1, 2, 9]

    r = definicao(x, y)

    print(r)

if __name__ == "__main__":
    main()
