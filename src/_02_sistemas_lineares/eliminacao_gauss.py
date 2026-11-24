import numpy as np

from utils import resolver_triangular_superior

# Recebe uma matriz e um vetor resultado (opcional).

# Retorna a matriz escalonada, vetor resultante, 
# matriz superior (U) e matriz de permutações.
def eliminacao_gauss(matriz, vetor_resultado=None):    
    A = np.array(matriz, dtype=float, copy=True)

    # Validações de A
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A matriz deve ser quadrada.")
    if A.shape[0] == 0:
        raise ValueError("A matriz não pode ser vazia.")
    if not(np.isfinite(A).all()):
        raise ValueError("A matriz deve conter apenas valores finitos.")

    num_linhas, num_colunas = A.shape 

    # Validações de b
    b = None
    if vetor_resultado is not None:
        b = np.array(vetor_resultado, dtype=float, copy=True)
        if b.ndim != 1 or b.size != num_linhas:
            raise ValueError("O vetor resultado está mal formatado.")
        if not(np.isfinite(b).all()):
            raise ValueError("O vetor b deve ter apenas valores finitos.")
    
    # Pivotamento parcial: escolhe a linha com o maior 
    # valor absoluto para ser o pivo 
    for col in range(num_colunas-1):
        pivo_linha = col + np.argmax(np.abs(A[col:, col])) 
        
        if np.isclose(A[pivo_linha, col], 0.0, atol=1e-12):
            raise np.linalg.LinAlgError("A matriz é singular ou tem um pivo nulo.")
        
        if pivo_linha != col:
            A[[col, pivo_linha]] = A[[pivo_linha, col]]

            if b is not None:
                b[[col, pivo_linha]] = b[[pivo_linha, col]]
            
        # Salvar elemento da diagonal principal
        diagonal = A[col][col]
        
        # Acessa todos os elementos abaixo da diagonal principal
        for row in range(col+1, num_linhas):
            # Acessa o elemento
            elemento = A[row][col]
            
            # Calcula o multiplicador
            multiplicador = elemento/diagonal

            #L[n] <-> L[n] - M[n][col] * L[col]
            A[row, col:] -= multiplicador * A[col, col:]

            if b is not None:
                b[row] -= multiplicador * b[col]
                
    if np.isclose(A[-1, -1], 0.0, atol=1e-12):
        raise np.linalg.LinAlgError("A matriz é singular ou tem pivo nulo.")

    return A, b

def gauss(A, b):
    U, b = eliminacao_gauss(A, b)
    x = resolver_triangular_superior(U, b)
    return x