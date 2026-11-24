import numpy as np
import matplotlib.pyplot as plt

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
        
        for lin in range(col+1, n):
            multiplicador = U[lin, col] / U[col, col]
            L[lin, col]   = multiplicador
            U[lin, col:] -= multiplicador * U[col, col:]
    
    return P, L, U

# Resolve o sistema: L * y = b, considerando L uma matriz
# triangular inferior.
def substituicao_regressiva(L, b):
    n = len(b)
    y = np.zeros(n)
    
    for i in range(n):
        soma = sum( L[i,j] * y[j] for j in range(i) )
        y[i] = (b[i] - soma) / L[i,i]

    return y

# Resolve o sistema: U * x = b, considerando U uma matriz
# triangular superior.
def substituicao_progressiva(U, y):
    n = len(y)
    x = np.zeros(n)
    
    for i in range(n):
        soma = sum( U[i,j] * x[j] for j in range(i+1, n) )
        x[i] = (y[i] - soma) / U[i,i]
    
    return x
    
# Interface para a execução completa do algorítmo.
def fatoracao_lu(A, b):
    P, L, U = fatorar_lu(A)
    b       = np.array(b, dtype=float)
    
    y = substituicao_progressiva(L, P@b)
    x = substituicao_regressiva(U, y)
    
    return x, P, L, U