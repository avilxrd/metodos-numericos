import numpy as np
import matplotlib.pyplot as plt

#
def simpson(func, a, b, n: int):
    if not isinstance(n, (int, np.integer)) or n < 2 or n % 2 != 0:
        raise ValueError("n deve ser um inteiro par >= 2.")
    
    if (a == b):
        return 0.0
   
    sinal = 1
    
    if a > b:
        a, b = b, a
        sinal = -1
    
    h = (b-a) / n
    soma = func(a) + func(b)
    
    for i in range(1, n):
        peso = 4 if i%2 == 1 else 2
        soma += peso * func(a+i*h)

    return sinal * (h/3) * soma

def simpson_tabelado(valores):
    if len(valores) < 3:
        raise ValueError("Sao necessários ao menos 3 pontos.")
    
    if len(valores) % 2 == 0:
        raise ValueError("A quantidade de pontos deve ser ímpar.")
    
    x = np.array([ponto[0] for ponto in valores], dtype=float)
    y = np.array([ponto[1] for ponto in valores], dtype=float)
    
    espacamentos = np.diff(x)

    if np.any(espacamentos <= 0):
        raise ValueError("Os valores de x precisam estar em ordem crescente.")

    if not np.allclose(espacamentos, espacamentos[0]):
        raise ValueError("Os pontos precisam estar igualmente espaçados.")

    h = espacamentos[0]

    soma = y[0] + y[-1]
    soma += 4 * np.sum(y[1:-1:2])
    soma += 2 * np.sum(y[2:-1:2])

    return (h / 3) * soma