import numpy as np

# Calcula as diferenças divididas.
def diferencas_divididas(x: list[float], y: list[float]) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    coeficientes = np.asarray(y, dtype=float).copy()
    
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
    valores  = np.asarray(valores, dtype=float)
    
    resultado = np.zeros_like(valores) + coeficientes[-1]
    
    for i in range(len(coeficientes) - 2, -1, -1):
        resultado = coeficientes[i] + (valores - x_pontos[i]) * resultado
    
    return resultado

# Interface para rodar o algoritmo completo.
def newton(x, y):
    return diferencas_divididas(x, y)
