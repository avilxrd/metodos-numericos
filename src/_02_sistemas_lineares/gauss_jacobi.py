import numpy as np

# Realiza as verificações necessárias para executar
# o algorítmo de Gauss-Jacob
def verificar_matriz(A):
    A = np.asarray(A, dtype=float)
    
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A matriz deve ser quadrada.")
    
    if np.any(np.diag(A) == 0):
        raise ValueError("A diagonal de A não pode conter zeros.")
    
    return A

# Define uma iteração do método.
def iteracao(A, b, x_atual):
    n = len(b)
    x_novo = np.zeros(n)
    
    for i in range(n):
        soma = 0.0

        for j in range(n):
            if j != i:
                soma += A[i,j] * x_atual[j]
        
        x_novo[i] = (b[i] - soma) / A[i,i]
    
    return x_novo

#
def gauss_jacobi(A, b, x_inicial, tolerancia=1e-10, max_iters=100):

    if not(tolerancia > 0):
        print(f"A tolerância deve ser positiva.")
        return

    A = verificar_matriz(A)
    b = np.asarray(b, dtype=float)
    
    if b.ndim != 1 or len(b) != A.shape[0]:
        raise ValueError("O vetor b precisa ter um valor para cada linha de A.")
    
    n = len(b)
    x = np.zeros(n) if x_inicial is None else np.asarray(x_inicial, dtype=float)
    
    if x.shape != (n, ):
        raise ValueError("x_inicial precisa ter o mesmo tamanho que b.")
    
    for i in range(1, max_iters+1):
        x_novo = iteracao(A, b, x)
        
        erro = np.linalg.norm(x_novo-x, ord=np.inf)
        
        if erro < tolerancia:
            return x_novo, i, erro
        
        x = x_novo

    print(f"Atingiu o número máximo de iterações: {max_iters}")
    return x, max_iters, erro