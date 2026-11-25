import numpy as np
import matplotlib.pyplot as plt

# Resolve o sistema triangular inferior L * x = b.
def resolver_triangular_inferior(L, b):
    L = np.asarray(L, dtype=float)
    b = np.asarray(b, dtype=float)
    if L.ndim != 2 or L.shape[0] != L.shape[1] or b.ndim != 1 or b.size != L.shape[0]:
        raise ValueError("L deve ser quadrada e compatível com b.")
    if not np.isfinite(L).all() or not np.isfinite(b).all():
        raise ValueError("L e b devem conter apenas valores finitos.")

    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        soma = sum(L[i, j] * x[j] for j in range(i))
        
        if np.isclose(L[i, i], 0.0, atol=1e-12):
            raise ValueError("Pivô nulo ou muito próximo de zero.")
        
        x[i] = (b[i] - soma) / L[i, i]

    return x

# Resolve o sistema triangular superior U * x = b.
def resolver_triangular_superior(U, b):
    U = np.asarray(U, dtype=float)
    b = np.asarray(b, dtype=float)
    if U.ndim != 2 or U.shape[0] != U.shape[1] or b.ndim != 1 or b.size != U.shape[0]:
        raise ValueError("U deve ser quadrada e compatível com b.")
    if not np.isfinite(U).all() or not np.isfinite(b).all():
        raise ValueError("U e b devem conter apenas valores finitos.")

    n = len(b)
    x = np.zeros(n)
    
    for i in range(n - 1, -1, -1):
        soma = sum(U[i, j] * x[j] for j in range(i + 1, n))
        
        if np.isclose(U[i, i], 0.0, atol=1e-12):
            raise ValueError("Pivô nulo ou muito próximo de zero.")
        
        x[i] = (b[i] - soma) / U[i, i]
    
    return x

def _salvar_e_mostrar_grafico(fig, nome: str) -> None:
    fig.savefig(f"img/{nome}.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(fig)

def plotar_ajuste_mmq(x, y, coeficientes) -> None:
    """Exibe os pontos e o polinômio calculado por mínimos quadrados."""
    fig, ax = plt.subplots()
    x_curva = np.linspace(min(x), max(x), 100)
    y_curva = np.polyval(coeficientes, x_curva)
    ax.scatter(x, y, label="Pontos tabelados")
    ax.plot(x_curva, y_curva, color="red", label="Polinômio MMQ")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Mínimos Quadrados")
    ax.legend()
    ax.grid(True)
    _salvar_e_mostrar_grafico(fig, "mmq")

def plotar_interpolacao_definicao(x, y, coeficientes) -> None:
    """Exibe os pontos e o polinômio interpolador por definição."""
    fig, ax = plt.subplots()
    x_curva = np.linspace(min(x), max(x), 100)
    y_curva = np.polyval(np.asarray(coeficientes)[::-1], x_curva)
    ax.plot(x_curva, y_curva, color="red", label="Interpolação por definição")
    ax.scatter(x, y, label="Pontos tabelados")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Interpolação por Definição")
    ax.legend()
    ax.grid(True)
    _salvar_e_mostrar_grafico(fig, "interpol_def")

def plotar_interpolacao_newton(x, y, coeficientes) -> None:
    """Exibe os pontos e o polinômio interpolador de Newton."""
    x = np.asarray(x, dtype=float)
    coeficientes = np.asarray(coeficientes, dtype=float)
    fig, ax = plt.subplots()
    x_curva = np.linspace(min(x), max(x), 100)
    y_curva = np.zeros_like(x_curva) + coeficientes[-1]
    for i in range(len(coeficientes) - 2, -1, -1):
        y_curva = coeficientes[i] + (x_curva - x[i]) * y_curva
    ax.plot(x_curva, y_curva, color="red", label="Polinômio de Newton")
    ax.scatter(x, y, label="Pontos tabelados", zorder=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Interpolação pelo Polinômio de Newton")
    ax.legend()
    ax.grid(True)
    _salvar_e_mostrar_grafico(fig, "interpol_newton")

def plotar_trapezio(func, a: float, b: float, n: int) -> None:
    """Exibe a função, as aproximações lineares e as áreas dos trapézios."""
    fig, ax = plt.subplots()
    if a == b:
        ax.scatter([a], [func(a)], color="C0", label="Ponto no intervalo")
        titulo = "Regra dos Trapézios (intervalo de comprimento zero)"
    else:
        x_nos = np.linspace(a, b, n + 1)
        y_nos = np.asarray([func(float(xi)) for xi in x_nos], dtype=float)
        x_curva = np.linspace(min(a, b), max(a, b), max(200, n * 20 + 1))
        y_curva = np.asarray([func(float(xi)) for xi in x_curva], dtype=float)
        ax.plot(x_curva, y_curva, color="C0", label="f(x)")
        ax.plot(x_nos, y_nos, "o--", color="C1", label="Aproximação por trapézios")
        for i in range(n):
            ax.fill_between(
                [x_nos[i], x_nos[i + 1]], [y_nos[i], y_nos[i + 1]], 0,
                color="C1", alpha=0.2,
            )
        titulo = f"Regra dos Trapézios ({n} subintervalos)"
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(titulo)
    ax.legend()
    ax.grid(True, alpha=0.3)
    _salvar_e_mostrar_grafico(fig, "trapezio")

def plotar_trapezio_tabelado(valores) -> None:
    """Exibe pontos tabelados e áreas dos trapézios consecutivos."""
    x, y = np.asarray(valores, dtype=float).T
    fig, ax = plt.subplots()
    ax.plot(x, y, "o--", color="C0", label="Pontos tabelados")
    for i in range(len(x) - 1):
        ax.fill_between([x[i], x[i + 1]], [y[i], y[i + 1]], 0, color="C1", alpha=0.2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Regra dos Trapézios com pontos tabelados")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _salvar_e_mostrar_grafico(fig, "trapezio")

def _plotar_parabolas_simpson(x, y, func=None):
    fig, ax = plt.subplots()
    if func is not None:
        x_curva = np.linspace(x[0], x[-1], max(200, (len(x) - 1) * 20 + 1))
        y_curva = np.asarray([func(float(xi)) for xi in x_curva], dtype=float)
        ax.plot(x_curva, y_curva, color="C0", label="f(x)")
    for i in range(0, len(x) - 2, 2):
        coeficientes = np.polyfit(x[i:i + 3], y[i:i + 3], 2)
        xx = np.linspace(x[i], x[i + 2], 60)
        yy = np.polyval(coeficientes, xx)
        ax.plot(xx, yy, color="C1", label="Parábolas de Simpson" if i == 0 else None)
        ax.fill_between(xx, yy, 0, color="C1", alpha=0.2)
    ax.scatter(x, y, color="C2", zorder=3, label="Pontos de amostragem")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig, ax

def plotar_simpson(func, a, b, n: int) -> None:
    """Exibe a função e as parábolas quadráticas da regra 1/3."""
    if a == b:
        fig, ax = plt.subplots()
        ax.scatter([a], [func(a)], color="C0", label="Ponto no intervalo")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Regra 1/3 de Simpson (intervalo de comprimento zero)")
        ax.legend()
        ax.grid(True, alpha=0.3)
    else:
        x = np.linspace(min(a, b), max(a, b), n + 1)
        y = np.asarray([func(float(xi)) for xi in x], dtype=float)
        fig, ax = _plotar_parabolas_simpson(x, y, func)
        ax.set_title(f"Regra 1/3 de Simpson ({n} subintervalos)")
    _salvar_e_mostrar_grafico(fig, "simpson")

def plotar_simpson_tabelado(valores) -> None:
    """Exibe pontos tabelados e as parábolas da regra 1/3 de Simpson."""
    x, y = np.asarray(valores, dtype=float).T
    fig, ax = _plotar_parabolas_simpson(x, y)
    ax.set_title("Regra 1/3 de Simpson com pontos tabelados")
    _salvar_e_mostrar_grafico(fig, "simpson")
