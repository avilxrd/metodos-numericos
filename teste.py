import numpy as np

import src.sistemas_lineares.eliminacao_gauss as sleg

A = np.array([
[4, 4, 5],
[1, 5, 6],
[2, 3, 6],
], dtype=float)

b = np.array([12, 14, 22], dtype=float)

matriz, res, L, perm = sleg.eliminacao_gauss(A,b)

print(matriz)
print(res)

x = sleg.retrossubstituicao(matriz, res)
print(x)