from __future__ import annotations

import curses
import math
from dataclasses import dataclass
from typing import Callable

# Imports de funções
from src._02_sistemas_lineares.eliminacao_gauss import gauss

@dataclass(frozen=True)
class MetodoItem:
    categoria: str
    nome: str
    acao: Callable[[], None]


def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).strip().replace(",", "."))
        except ValueError:
            print("  [!] Entrada inválida. Digite um número.")


def ler_int(mensagem: str, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo is not None and valor < minimo:
                print(f"  [!] Digite um valor >= {minimo}.")
                continue
            return valor
        except ValueError:
            print("  [!] Entrada inválida. Digite um inteiro.")


def ler_funcao(mensagem: str = "Digite f(x) (ex: x**3 - x - 2): ") -> Callable[[float], float]:
    ambiente = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    ambiente["abs"] = abs

    while True:
        expr = input(mensagem).strip()
        try:
            codigo = compile(expr, "<funcao>", "eval")
            for nome in codigo.co_names:
                if nome != "x" and nome not in ambiente:
                    raise NameError(f"Símbolo não permitido: '{nome}'")

            def f(x: float, _code=codigo, _env=ambiente) -> float:
                escopo = dict(_env)
                escopo["x"] = x
                return float(eval(_code, {"__builtins__": {}}, escopo))

            f(1.0)
            return f
        except Exception as erro:
            print(f"  [!] Expressão inválida ({erro}). Tente novamente.")


def ler_sistema_linear() -> tuple[list[list[float]], list[float]]:
    n = ler_int("Dimensão n do sistema: ", minimo=1)
    print("Digite cada linha da matriz A separada por espaço:")
    A: list[list[float]] = []
    for i in range(n):
        while True:
            partes = input(f"  Linha {i + 1}: ").strip().replace(",", ".").split()
            if len(partes) != n:
                print(f"  [!] Esperados {n} valores, mas recebeu {len(partes)}.")
                continue
            try:
                A.append([float(p) for p in partes])
                break
            except ValueError:
                print("  [!] Use apenas números.")

    print("Digite o vetor b:")
    b = [ler_float(f"  b[{i + 1}]: ") for i in range(n)]
    return A, b


# --- Handlers dos métodos ---

def run_eliminacao_gauss() -> None:
    print("\nEliminação de Gauss\n")
    A, b = ler_sistema_linear()
    solucao = gauss(A, b)
    print(f"A = {A}        \n"
          f"b = {b}        \n" 
          f"Sol: {solucao} \n")


def run_fatoracao_lu() -> None:
    print("\n=== Fatoração LU ===\n")
    A, b = ler_sistema_linear()
    # L, U, x = fatoracao_lu(A, b)
    print("\n[TODO] Conectar fatoracao_lu(A, b) de src/_02_sistemas_lineares/fatoracao_lu.py")
    print(f"A = {A}\nb = {b}")


def run_exemplo_raiz() -> None:
    print("\n=== Método de Raízes ===\n")
    f = ler_funcao()
    a = ler_float("Limite a: ")
    b = ler_float("Limite b: ")
    tol = ler_float("Tolerância (ex: 1e-6): ")
    print(f"\n[TODO] Conectar método de src/_01_raizes/ | f({a})={f(a):.6g}, f({b})={f(b):.6g}, tol={tol}")


OPCOES: list[MetodoItem] = [
    MetodoItem("01. Raízes", "Bisseção", run_exemplo_raiz),
    MetodoItem("01. Raízes", "Falsa Posição", run_exemplo_raiz),
    MetodoItem("01. Raízes", "Newton-Raphson", run_exemplo_raiz),
    MetodoItem("01. Raízes", "Secantes", run_exemplo_raiz),
    MetodoItem("02. Sistemas Lineares", "Eliminação de Gauss", run_eliminacao_gauss),
    MetodoItem("02. Sistemas Lineares", "Fatoração LU", run_fatoracao_lu),
    MetodoItem("02. Sistemas Lineares", "Gauss-Jacob", run_fatoracao_lu),
    MetodoItem("03. Ajuste de Curvas", "Mínimos Quadrados", run_fatoracao_lu),
    MetodoItem("04. Interpolação Polinomial", "Definição", run_fatoracao_lu),
    MetodoItem("04. Interpolação Polinomial", "Polinômio de Newton", run_fatoracao_lu),
    MetodoItem("05. Integração Numérica", "Regra dos Trapézios", run_fatoracao_lu),
    MetodoItem("05. Integração Numérica", "1/3 de Simpson", run_fatoracao_lu),
    MetodoItem("Sistema", "Sair", lambda: None),
]


def _menu_curses(stdscr: curses.window) -> int | None:
    curses.curs_set(0)
    stdscr.keypad(True)
    idx = 0

    while True:
        stdscr.clear()
        altura, largura = stdscr.getmaxyx()

        titulo = "MÉTODOS NUMÉRICOS"
        subtitulo = "Use ↑ / ↓ para navegar, ENTER para selecionar, ESC ou q para sair"
        stdscr.addstr(0, 2, titulo[: largura - 4], curses.A_BOLD)
        if altura > 1:
            stdscr.addstr(1, 2, subtitulo[: largura - 4], curses.A_DIM)

        linha = 3
        categoria_atual = ""

        for i, item in enumerate(OPCOES):
            if item.categoria != categoria_atual:
                categoria_atual = item.categoria
                if linha < altura - 1:
                    stdscr.addstr(linha, 2, f"[{categoria_atual}]"[: largura - 4], curses.A_BOLD)
                    linha += 1

            if linha >= altura - 1:
                break

            marcador = "▶ " if i == idx else "  "
            texto = f"{marcador}{item.nome}"[: largura - 5]
            # A_REVERSE deixa a linha sombreada/destacada
            estilo = curses.A_REVERSE | curses.A_BOLD if i == idx else curses.A_NORMAL
            stdscr.addstr(linha, 4, texto, estilo)
            linha += 1

        stdscr.refresh()
        tecla = stdscr.getch()

        if tecla == curses.KEY_UP:
            idx = (idx - 1) % len(OPCOES)
        elif tecla == curses.KEY_DOWN:
            idx = (idx + 1) % len(OPCOES)
        elif tecla in (curses.KEY_ENTER, 10, 13):
            return idx
        elif tecla in (27, ord("q"), ord("Q")):
            return None


def main() -> None:
    while True:
        try:
            selecionado = curses.wrapper(_menu_curses)
        except curses.error:
            # Fallback caso rode em terminal sem suporte a curses (ex: alguns terminais no Windows)
            for i, item in enumerate(OPCOES, start=1):
                print(f"{i}) [{item.categoria}] {item.nome}")
            escolha = ler_int("Escolha o número: ", minimo=1)
            selecionado = escolha - 1 if escolha <= len(OPCOES) else None

        if selecionado is None or OPCOES[selecionado].nome == "Sair":
            print("Saindo...")
            break

        print("\033[2J\033[H", end="")
        try:
            OPCOES[selecionado].acao()
        except KeyboardInterrupt:
            print("\n[!] Operação cancelada.")
        except Exception as erro:
            print(f"\n[!] Erro: {erro}")

        input("\nPressione ENTER para voltar ao menu...")


if __name__ == "__main__":
    main()