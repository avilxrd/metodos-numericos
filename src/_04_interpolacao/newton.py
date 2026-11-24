import numpy as np
import matplotlib.pyplot as plt

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

# Plota os pontos e o polinômio interpolador.
def plotar_interpolacao(x, y, coeficientes):
    fig, ax = plt.subplots()
    x_curva = np.linspace(min(x), max(x), 100)
    y_curva = avaliar_newton(x, coeficientes, x_curva)

    ax.plot(x_curva, y_curva, color="red", label="Polinômio de Newton")
    ax.scatter(x, y, label="Pontos tabelados", zorder=2)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Interpolação pelo Polinômio de Newton")
    ax.legend()
    ax.grid(True)

    fig.savefig("img/interpol_newton.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(fig)
    
# Interface para rodar o algoritmo completo.
def newton(x, y):
    coeficientes = diferencas_divididas(x, y)
    plotar_interpolacao(x, y, coeficientes)

    return coeficientes

# Interface de teste.
def main():
    x = [-1, 0, 1, 2]
    y = [0, 1, 2, 9]

    coeficientes = newton(x, y)

    print("Coeficientes de Newton:", coeficientes)


if __name__ == "__main__":
    main()
