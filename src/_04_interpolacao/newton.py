import numpy as np

# Calcula as diferenças divididas.
def diferencas_divididas(x: list[float], y: list[float]) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    coeficientes = np.asarray(y, dtype=float).copy()

    if x.ndim != 1 or coeficientes.ndim != 1:
        raise ValueError("x e y devem ser vetores.")
    if x.size == 0:
        raise ValueError("É necessário informar ao menos um ponto.")
    if not np.isfinite(x).all() or not np.isfinite(coeficientes).all():
        raise ValueError("Os pontos devem conter apenas valores finitos.")
    
    if len(x) != len(coeficientes):
        raise ValueError("x e y precisam ter o mesmo número de elementos.")
    
    if len(np.unique(x)) != len(x):
        raise ValueError("Os valores de x precisam ser distintos.")
    
    n = len(x)
    
    for ord in range(1, n):
        for i in range(n-1, ord-1, -1):
            coeficientes[i] = (coeficientes[i] - coeficientes[i-1]) / (x[i] - x[i-ord])
    
    return coeficientes

# Avalia o polinômio de Newton em x.
def avaliar_newton(x_pontos: list[float], coeficientes: np.ndarray, valores):
    x_pontos = np.asarray(x_pontos, dtype=float)
    coeficientes = np.asarray(coeficientes, dtype=float)
    valores  = np.asarray(valores, dtype=float)

    if x_pontos.ndim != 1 or coeficientes.ndim != 1:
        raise ValueError("x_pontos e coeficientes devem ser vetores.")
    if x_pontos.size == 0 or x_pontos.size != coeficientes.size:
        raise ValueError("x_pontos e coeficientes devem ter o mesmo tamanho não nulo.")
    if not np.isfinite(x_pontos).all() or not np.isfinite(coeficientes).all() or not np.isfinite(valores).all():
        raise ValueError("Pontos, coeficientes e valores devem ser finitos.")
    
    resultado = np.zeros_like(valores) + coeficientes[-1]
    
    for i in range(len(coeficientes) - 2, -1, -1):
        resultado = coeficientes[i] + (valores - x_pontos[i]) * resultado
    
    return resultado

# Interface para rodar o algoritmo completo.
def newton(x, y):
    return diferencas_divididas(x, y)
