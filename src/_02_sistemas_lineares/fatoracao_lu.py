import numpy as np
import matplotlib.pyplot as plt

from utils import resolver_triangular_superior, resolver_triangular_inferior

# Fatora a matriz original nas matrizes L (lower), U (upper) e P
# Estratégia de pivotamento: pivotamento parcial.
def fatorar_lu(A, tolerancia=1e-12):
    A = np.array(A, dtype=float)
    n = A.shape[0]
    
    if A.ndim != 2 or A.shape[1] != n:
        raise ValueError("A matriz precisa ser quadrada.")
    
    U = A.copy()
    L = np.eye(n)
    P = np.eye(n)
    
    for col in range(n):
        linha_pivo = col + np.argmax(np.abs(U[col:, col]))
        
        if abs(U[linha_pivo, col]) < tolerancia:
            raise ValueError("A matriz é singular ou quase singular.")
        
        if linha_pivo != col:
            U[[col, linha_pivo]] = U[[linha_pivo, col]]
            P[[col, linha_pivo]] = P[[linha_pivo, col]]
            
            if col > 0:
                L[[col, linha_pivo], :col] = (L[[linha_pivo, col], :col])
        
        for row in range(col+1, n):
            multiplicador = U[row, col] / U[col, col]
            L[row, col]   = multiplicador
            U[row, col:] -= multiplicador * U[col, col:]
    
    return P, L, U
    
# Interface para a execução completa do algorítmo.
def fatoracao_lu(A, b):
    P, L, U = fatorar_lu(A)
    b       = np.array(b, dtype=float)
    
    y = resolver_triangular_inferior(L, P@b)
    x = resolver_triangular_superior(U, y)
    
    return x, P, L, U