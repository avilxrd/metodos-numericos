import numpy as np

# Recebe uma matriz
# Retorna uma tupla contendo
#   A matriz resultante
#   Uma matriz com os multiplicadores
def eliminacao_gauss(matriz, vetor_resultado=None):
    
    # Verificações na Matriz A
    A = np.array(matriz, dtype=float, copy=True)
    
    if A.ndim != 2:
        raise ValueError("A matriz deve ter 2 dimensoes.")

    num_linhas, num_colunas = A.shape 
    if num_linhas != num_colunas:
        raise ValueError("A matriz deve ser quadrada.")
    
    # Verificações no Vetor resultado b
    b = None
    if vetor_resultado is not None:
        b = np.array(vetor_resultado, dtype=float, copy=True)
        if b.ndim != 1 or b.size != num_linhas:
            raise ValueError("O vetor resultado está mal formatado.")
    
    #
    L = np.eye(num_linhas)
    permutacoes = np.arange(num_linhas)
    
    # 1) Escolher o elemento
    for col in range(num_colunas-1):
        # Pivotamento parcial: escolhe a linha com o maior 
        # valor absoluto para ser o pivo 
        pivo_linha = col + np.argmax(np.abs(A[col:, col])) 
        
        if np.isclose(A[pivo_linha, col], 0.0):
            raise np.linalg.LinAlgError("A matriz é singular ou tem um pivo nulo.")
        
        if pivo_linha != col:
            A[[col, pivo_linha]] = A[[pivo_linha, col]]
            permutacoes[[col, pivo_linha]] = permutacoes[[pivo_linha, col]]
        
            if b is not None:
                b[[col, pivo_linha]] = b[[pivo_linha, col]]
            
            L[[col, pivo_linha], :col] = L[[pivo_linha, col], :col]
            
        # Salvar elemento da diagonal principal
        diagonal = A[col][col]
        
        # Acessa todos os elementos abaixo da diagonal principal
        for row in range(col+1, num_linhas):
            # Acessa o elemento
            elemento = A[row][col]
            
            # Calcula o multiplicador
            multiplicador = elemento/diagonal

            L[row, col]  =  multiplicador

            #L[n] <-> L[n] - M[n][col] * L[col]
            A[row, col:] -= multiplicador * A[col, col:]

            if b is not None:
                b[row] -= multiplicador * b[col]
                
    if np.isclose(A[-1, -1], 0.0):
        raise np.linalg.LinAlgError("A matriz é singular ou tem pivo nulo.")

    return A, b, L, permutacoes


# Recebe a matriz aumentada (matriz + vetor de solução) após o escalonamento
# e realiza a retrossubstituicao para obter a solução do sistema.
def retrossubstituicao(U, b):
    U = np.asarray(U, dtype=float)
    b = np.asarray(b, dtype=float)

    n = U.shape[0]

    if U.ndim != 2 or U.shape[1] != n:
        raise ValueError("U deve ser quadrada.")
    if b.ndim != 1 or b.size != n:
        raise ValueError("b deve ter um valor para cada linha de U.")

    x = np.zeros(n)

    for i in range(n-1, -1, -1):
        if np.isclose(U[i, i], 0.0):
            raise np.linalg.LinAlgError("U tem pivô nulo. Não é possível fazer retrossubstituição.")

        soma = np.dot(U[i, i + 1:], x[i + 1:])
        x[i] = (b[i] - soma) / U[i, i]

    return x

def gauss(A, b):
    U, b, L, p = eliminacao_gauss(A, b)
    x = retrossubstituicao(U, b)
    return x