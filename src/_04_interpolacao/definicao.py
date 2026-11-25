import numpy as np

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

# Interface para rodar o algorítmo completo.
# Monta a matriz, calcula os coeficientes
# utilizando o método de Gauss implementado.
def definicao(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x e y devem ser vetores.")
    if x.size == 0 or x.size != y.size:
        raise ValueError("x e y devem ter o mesmo tamanho não nulo.")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Os pontos devem conter apenas valores finitos.")
    if len(np.unique(x)) != len(x):
        raise ValueError("Os valores de x devem ser distintos.")

    V = montar_matriz(x)
    coeficientes = gauss(V, y)
    return coeficientes
