import numpy as np

# Realiza as verificações necessárias para executar
# o algorítmo de Gauss-Jacobi.
def verificar_matriz(A):
    A = np.asarray(A, dtype=float)
    
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A matriz deve ser quadrada.")

    if A.shape[0] == 0:
        raise ValueError("A matriz não pode ser vazia.")

    if not np.isfinite(A).all():
        raise ValueError("A matriz deve conter apenas valores finitos.")
    
    if np.any(np.isclose(np.diag(A), 0.0, atol=1e-12)):
        raise ValueError("A diagonal de A não pode conter valores nulos ou muito próximos de zero.")
    
    return A

# Define uma iteração do método.
def iteracao(A, b, x_atual):
    n = len(b)
    x_novo = np.zeros(n)
    
    # Isolar a variável da diagonal principal em cada linha.
    # ex: a*x + b*y + c*z = res_1
    #     soma = b * y_atual + c * z_atual
    #     x0 = (res_1 - soma) / a
    for i in range(n):
        soma = 0.0

        for j in range(n):
            if j != i:
                soma += A[i,j] * x_atual[j]
        
        x_novo[i] = (b[i] - soma) / A[i,i]
    
    return x_novo

#
def gauss_jacobi(A, b, x_inicial, tolerancia=1e-10, max_iters=100):
    if not np.isfinite(tolerancia) or tolerancia <= 0:
        raise ValueError("A tolerância deve ser finita e positiva.")
    if isinstance(max_iters, (bool, np.bool_)) or not isinstance(max_iters, (int, np.integer)) or max_iters < 1:
        raise ValueError("max_iters deve ser um inteiro positivo.")

    A = verificar_matriz(A)
    b = np.asarray(b, dtype=float)
    
    if b.ndim != 1 or len(b) != A.shape[0]:
        raise ValueError("O vetor b precisa ter um valor para cada linha de A.")
    if not np.isfinite(b).all():
        raise ValueError("O vetor b deve conter apenas valores finitos.")
    
    n = len(b)
    x = np.zeros(n) if x_inicial is None else np.asarray(x_inicial, dtype=float)
    
    if x.shape != (n, ):
        raise ValueError("x_inicial precisa ter o mesmo tamanho que b.")
    if not np.isfinite(x).all():
        raise ValueError("x_inicial deve conter apenas valores finitos.")
    
    for i in range(1, max_iters+1):
        x_novo = iteracao(A, b, x)
        
        # Calcula quanto a variável que mais mudou variou entre
        # a iteração anterior e a atual (x - x_novo). -> Norma infinita.
        erro = np.linalg.norm(x_novo-x, ord=np.inf)
        
        if erro < tolerancia:
            return x_novo, i, erro
        
        x = x_novo
        
    print(f"Atingiu o número máximo de iterações: {max_iters}")
    return x, max_iters, erro
