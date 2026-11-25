import numpy as np

# Recebe uma função. Calcula a integral numérica através
# da fórmula vista em sala de aula.
def trapezio(func, a: float, b: float, n: int):
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError("n deve ser um inteiro positivo.")
    if not np.isfinite(a) or not np.isfinite(b):
        raise ValueError("Os limites de integração devem ser finitos.")
    
    if a == b:
        return 0.0

    sinal = 1
    
    if a > b:
        c = a
        a = b
        b = c
        sinal = -1

    h = (b - a) / n

    integral = (h/2) * (
        func(a)                                      + 
        2*sum( func(a + (i*h)) for i in range(1,n) ) +
        func(b)
    )
    
    return integral * sinal

# Recebe os dados tabelados. Os dados não precisam estar
# igualmente espaçados. Calcula iterativamente a integral.
# valores: lista de tuplas (x, y)
def trapezio_tabelado(valores):
    valores = np.asarray(valores, dtype=float)
    if valores.ndim != 2 or valores.shape[1] != 2:
        raise ValueError("Informe os pontos como pares (x, y).")
    if valores.shape[0] < 2:
        raise ValueError("São necessários pelo menos dois pontos.")
    if not np.isfinite(valores).all():
        raise ValueError("Os pontos devem conter apenas valores finitos.")
    if np.any(np.diff(valores[:, 0]) <= 0):
        raise ValueError("Os valores de x devem estar em ordem crescente.")
    
    integral = 0
    
    for i in range(len(valores) - 1):
        x0, y0 = valores[i]
        x1, y1 = valores[i + 1]

        h = x1 - x0
        
        integral += (h/2) * (y0 + y1)

    return integral
