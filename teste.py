import numpy as np

import src.sistemas_lineares.fatoracao_lu as slfu
import src.sistemas_lineares.eliminacao_gauss as sleg

A = np.array([
[4, 4, 5],
[1, 5, 6],
[2, 3, 6],
], dtype=float)

b = np.array([12, 14, 22], dtype=float)

X, c = sleg.eliminacao_gauss(A)

print(X)

print(c)