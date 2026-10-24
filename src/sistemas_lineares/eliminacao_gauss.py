import numpy as np

#recebe uma matriz (pode ser aumentada ou nao)
#retorna uma tupla contendo
#   1. a matriz resultante
#   2. uma lista contendo os multiplicadores (sera usado na fat. lu)
def eliminacao_gauss(A, b = None) -> tuple[list[list[float]], list[float]]:
    A = np.array(A, dtype=float, copy=True)
    b = np.array(b, dtype=float, copy=True)
    
    multiplicadores = []

    num_linhas  = len(A)
    num_colunas = len(A[0]) if A.any() else 0      
    
    #1) escolher o elemento
    for col in range(num_colunas):
        
        #salvar elemento da diagonal principal
        diagonal = A[col][col]
        
        #acessa todos os elementos abaixo da diagonal principal
        for row in range(col+1, num_linhas):
            #acessa o elemento
            elemento = A[row][col]
            print(A[row][col])
            
            #calcula o multiplicador
            multiplicador = elemento/diagonal

            #adiciona o multiplicado a lista de retorno
            multiplicadores.append(multiplicador)
            
            #L[n] <-> L[n] - M[n][col] * L[col]
            A[row] = A[row] - multiplicador * A[col]

    return (A, multiplicadores)