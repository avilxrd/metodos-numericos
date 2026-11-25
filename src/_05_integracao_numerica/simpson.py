import numpy as np

# Regra composta 1/3 de Simpson para uma função.
def simpson(func, a, b, n: int):
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)) or n < 2 or n % 2 != 0:
        raise ValueError("n deve ser um inteiro par >= 2.")
    if not np.isfinite(a) or not np.isfinite(b):
        raise ValueError("Os limites de integração devem ser finitos.")
    
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


# Regra 1/3 de Simpson composta para valores tabelados uniformemente espaçados.
def simpson_tabelado(valores):
    valores = np.asarray(valores, dtype=float)
    if valores.ndim != 2 or valores.shape[1] != 2:
        raise ValueError("Informe os pontos como pares (x, y).")
    if valores.shape[0] < 3:
        raise ValueError("Sao necessários ao menos 3 pontos.")
    
    if valores.shape[0] % 2 == 0:
        raise ValueError("A quantidade de pontos deve ser ímpar.")
    
    if not np.isfinite(valores).all():
        raise ValueError("Os pontos devem conter apenas valores finitos.")

    x = valores[:, 0]
    y = valores[:, 1]
    
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
