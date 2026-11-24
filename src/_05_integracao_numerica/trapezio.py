# Recebe uma função. Calcula a integral numérica através
# da fórmula vista em sala de aula.
def trapezio(func, a: float, b: float, n: int):
    if n < 1:
        raise ValueError("Entrada inválida. O valor de n é menor que 1.")
    
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
    if len(valores) < 2:
        return
    
    integral = 0
    
    for i in range(len(valores) - 1):
        x0, y0 = valores[i]
        x1, y1 = valores[i+1]

        h = x1 - x0
        
        integral += (h/2) * (y0 + y1)

    return integral

# 
def main():

    dados = [
        (0, 0),
        (0.1, 0.2),
        (0.4, 0.8),
        (0.7, 1.4),
        (1.0, 2.0)
    ]

    integral = trapezio_tabelado(dados)

    print(f'Integral: {integral}')

if __name__ == "__main__":
    main()