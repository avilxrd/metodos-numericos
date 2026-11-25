from __future__ import annotations

import curses
import math
import textwrap
from dataclasses import dataclass
from typing import Callable

import numpy as np

from src._02_sistemas_lineares.eliminacao_gauss import gauss
from src._02_sistemas_lineares.fatoracao_lu import fatoracao_lu
from src._02_sistemas_lineares.gauss_jacobi import gauss_jacobi
from src._03_ajuste_curvas.mmq import ajustar_curva
from src._04_interpolacao.definicao import definicao
from src._04_interpolacao.newton import diferencas_divididas, avaliar_newton
from src._05_integracao_numerica.trapezio import trapezio, trapezio_tabelado
from src._05_integracao_numerica.simpson import simpson, simpson_tabelado
from utils import (
    plotar_ajuste_mmq,
    plotar_interpolacao_definicao,
    plotar_interpolacao_newton,
    plotar_trapezio,
    plotar_trapezio_tabelado,
    plotar_simpson,
    plotar_simpson_tabelado,
)


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


def escolher_opcao(titulo: str, opcoes: list[str]) -> int:
    """Mostra uma lista navegável e retorna o índice, ou -1 para voltar."""
    try:
        return curses.wrapper(_menu_escolha_curses, titulo, opcoes)
    except curses.error:
        print(f"\n=== {titulo.upper()} ===")
        for i, opcao in enumerate(opcoes, start=1):
            print(f"  {i:>2}) {opcao}")
        print("   0) Voltar")
        while True:
            escolha = ler_int("Selecione uma opção: ", minimo=0)
            if escolha <= len(opcoes):
                return escolha - 1
            print(f"  [!] Escolha um número entre 0 e {len(opcoes)}.")


def _menu_escolha_curses(stdscr: curses.window, titulo: str, opcoes: list[str]) -> int:
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    stdscr.keypad(True)
    idx = 0
    total = len(opcoes) + 1  # A última opção sempre retorna ao menu anterior.
    while True:
        stdscr.clear()
        altura, largura = stdscr.getmaxyx()

        def escrever(y: int, x: int, texto: str, estilo: int = curses.A_NORMAL) -> None:
            if y < 0 or y >= altura or largura <= 1 or x >= largura - 1:
                return
            try:
                stdscr.addnstr(y, x, texto, max(0, largura - x - 1), estilo)
            except curses.error:
                pass

        escrever(0, 2, titulo.upper(), curses.A_BOLD)
        escrever(1, 2, "↑/↓ navegar   Enter selecionar   Esc voltar", curses.A_DIM)
        escrever(2, 2, "─" * max(0, largura - 5), curses.A_DIM)

        largura_texto = max(10, largura - 8)
        itens = [textwrap.wrap(opcao, width=largura_texto) or [""] for opcao in opcoes]
        itens.append(["← Voltar"])
        linhas_disponiveis = max(1, altura - 4)
        inicio = idx
        while inicio > 0 and sum(len(itens[i]) for i in range(inicio, idx + 1)) < linhas_disponiveis:
            inicio -= 1
        linha = 3
        for i in range(inicio, total):
            if linha + len(itens[i]) > altura - 1:
                break
            estilo = curses.A_REVERSE | curses.A_BOLD if i == idx else curses.A_NORMAL
            for parte, texto in enumerate(itens[i]):
                marcador = ("› " if i == idx else "  ") if parte == 0 else "  "
                escrever(linha, 3, marcador + texto, estilo)
                linha += 1
        escrever(altura - 1, 2, f"{idx + 1}/{total}", curses.A_DIM)
        stdscr.refresh()

        tecla = stdscr.getch()
        if tecla == curses.KEY_UP:
            idx = (idx - 1) % total
        elif tecla == curses.KEY_DOWN:
            idx = (idx + 1) % total
        elif tecla in (curses.KEY_ENTER, 10, 13):
            return idx if idx < len(opcoes) else -1
        elif tecla in (27, ord("q"), ord("Q")):
            return -1


def escolher_dados(titulo: str, exemplos: dict[str, object]):
    nomes = list(exemplos)
    escolha = escolher_opcao(titulo, [*nomes, "Digitar meus próprios dados"])
    if escolha == -1:
        return None
    if escolha < len(nomes):
        return exemplos[nomes[escolha]]
    return "custom"


def ler_funcao(mensagem: str = "Digite f(x) (ex: x**3 - x - 2): ") -> Callable[[float], float]:
    ambiente = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    ambiente["abs"] = abs

    while True:
        print("Use x, operações + - * / **, abs() e funções de math como sin(), cos(), exp() e sqrt().")
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

            f.expressao = expr
            return f
        except Exception as erro:
            print(f"  [!] Expressão inválida ({erro}). Tente novamente.")


def ler_sistema_linear() -> tuple[list[list[float]], list[float]]:
    n = ler_int("Dimensão n do sistema: ", minimo=1)
    A: list[list[float]] = []
    print("Digite cada linha da matriz A separada por espaço:")
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


def obter_sistema():
    exemplos = {
        "A=[[4, 1, 1], [2, 5, 1], [1, 1, 3]], b=[6, 8, 4]":
            ([[4, 1, 1], [2, 5, 1], [1, 1, 3]], [6, 8, 4]),
        "A=[[0, 2], [1, 3]], b=[4, 7]":
            ([[0, 2], [1, 3]], [4, 7]),
        "A=[[10, 1, 1, 1], [2, 12, 1, 1], [1, 2, 15, 1], [1, 1, 2, 18]], b=[13, 16, 19, 22]": (
            [[10, 1, 1, 1], [2, 12, 1, 1], [1, 2, 15, 1], [1, 1, 2, 18]],
            [13, 16, 19, 22],
        ),
    }
    dados = escolher_dados("Sistema linear", exemplos)
    if dados == "custom":
        dados = ler_sistema_linear()
    if dados is not None:
        A, b = dados
        imprimir_sistema(A, b)
    return dados


# Mesmos conjuntos nos métodos que aceitam pontos (ajuste, interpolação e
# integração tabelada). As abscissas uniformes também atendem Simpson 1/3.
EXEMPLOS_PONTOS = {
    "Pontos [(0, 0), (0.5, 0.25), (1, 1), (1.5, 2.25), (2, 4)] (y=x²)":
        [(0, 0), (0.5, 0.25), (1, 1), (1.5, 2.25), (2, 4)],
    "Pontos [(0, 1), (0.5, 2), (1, 3), (1.5, 4), (2, 5)] (y=2x+1)":
        [(0, 1), (0.5, 2), (1, 3), (1.5, 4), (2, 5)],
    "Pontos [(0, 1), (0.5, 1.4), (1, 2.2), (1.5, 3.1), (2, 5.2)]":
        [(0, 1), (0.5, 1.4), (1, 2.2), (1.5, 3.1), (2, 5.2)],
}


def exemplos_pontos_integracao() -> dict[str, list[tuple[float, float]]]:
    # Simpson exige quantidade ímpar de pontos, espaçamento uniforme; os
    # conjuntos compartilhados satisfazem essas condições.
    return EXEMPLOS_PONTOS


def ler_pontos() -> tuple[list[float], list[float]]:
    n = ler_int("Quantidade de pontos: ", minimo=1)
    x, y = [], []
    print("Digite um par x y por linha (ex: 1.5 2.7):")
    for i in range(n):
        while True:
            entrada = input(f"  Ponto {i + 1}: ").strip().replace(",", ".").split()
            if len(entrada) != 2:
                print("  [!] Informe exatamente dois valores: x e y.")
                continue
            try:
                xi, yi = map(float, entrada)
                x.append(xi)
                y.append(yi)
                break
            except ValueError:
                print("  [!] Use números para x e y.")
    return x, y


def formatar_numero(valor: float) -> str:
    return f"{float(valor):.6g}"


def formatar_vetor(vetor) -> str:
    valores = np.asarray(vetor, dtype=float).ravel()
    return "[" + ", ".join(formatar_numero(v) for v in valores) + "]"


def formatar_matriz(matriz) -> str:
    linhas = np.asarray(matriz, dtype=float)
    if linhas.ndim != 2:
        return str(matriz)
    formatados = [[formatar_numero(v) for v in linha] for linha in linhas]
    larguras = [max(len(linha[j]) for linha in formatados) for j in range(linhas.shape[1])]
    return "\n".join(
        "[ " + "  ".join(valor.rjust(larguras[j]) for j, valor in enumerate(linha)) + " ]"
        for linha in formatados
    )


def imprimir_sistema(A, b) -> None:
    print("\nSistema informado:")
    print(f"A =\n{formatar_matriz(A)}")
    print(f"b = {formatar_vetor(b)}")


def imprimir_pontos(x, y) -> None:
    print("\nPontos informados:")
    print(f"{'i':>3}  {'x':>12}  {'y':>12}")
    for i, (xi, yi) in enumerate(zip(x, y), start=1):
        print(f"{i:>3}  {formatar_numero(xi):>12}  {formatar_numero(yi):>12}")


def formatar_polinomio(coeficientes, ordem: str = "decrescente") -> str:
    coeficientes = np.asarray(coeficientes, dtype=float).ravel()
    termos = []
    for i, coef in enumerate(coeficientes):
        potencia = len(coeficientes) - i - 1 if ordem == "decrescente" else i
        if np.isclose(coef, 0.0, atol=1e-14):
            continue
        magnitude = abs(coef)
        if potencia == 0:
            corpo = formatar_numero(magnitude)
        elif potencia == 1:
            corpo = ("" if np.isclose(magnitude, 1.0) else formatar_numero(magnitude)) + "x"
        else:
            corpo = ("" if np.isclose(magnitude, 1.0) else formatar_numero(magnitude)) + f"x^{potencia}"
        if not termos:
            termos.append(("-" if coef < 0 else "") + corpo)
        else:
            termos.append((" - " if coef < 0 else " + ") + corpo)
    return "".join(termos) if termos else "0"


def formatar_polinomio_newton(coeficientes, x_pontos) -> str:
    termos = []
    for i, coef in enumerate(np.asarray(coeficientes, dtype=float)):
        if np.isclose(coef, 0.0, atol=1e-14):
            continue
        fatores = "".join(f"(x - ({formatar_numero(xi)}))" for xi in x_pontos[:i])
        magnitude = abs(coef)
        corpo = ("" if fatores and np.isclose(magnitude, 1.0) else formatar_numero(magnitude)) + fatores
        if not fatores:
            corpo = formatar_numero(magnitude)
        if not termos:
            termos.append(("-" if coef < 0 else "") + corpo)
        else:
            termos.append((" - " if coef < 0 else " + ") + corpo)
    return "".join(termos) if termos else "0"


def obter_pontos(titulo: str, exemplos: dict[str, list[tuple[float, float]]]):
    dados = escolher_dados(titulo, exemplos)
    if dados == "custom":
        pontos = ler_pontos()
    elif dados is None:
        return None
    else:
        pontos = [p[0] for p in dados], [p[1] for p in dados]
    imprimir_pontos(*pontos)
    return pontos


def run_eliminacao_gauss() -> None:
    dados = obter_sistema()
    if dados is None:
        return
    A, b = dados
    print(f"\nSolução x = {formatar_vetor(gauss(A, b))}")


def run_fatoracao_lu() -> None:
    dados = obter_sistema()
    if dados is None:
        return
    A, b = dados
    x, P, L, U = fatoracao_lu(A, b)
    print(f"\nSolução x = {formatar_vetor(x)}")
    print(f"\nP =\n{formatar_matriz(P)}\n\nL =\n{formatar_matriz(L)}\n\nU =\n{formatar_matriz(U)}")


def run_gauss_jacobi() -> None:
    dados = obter_sistema()
    if dados is None:
        return
    A, b = dados
    x0 = [0.0] * len(b)
    tolerancia = ler_float("Tolerância: ")
    max_iters = ler_int("Máximo de iterações: ", minimo=1)
    x, iteracoes, erro = gauss_jacobi(A, b, x0, tolerancia, max_iters)
    print(f"\nSolução aproximada x = {formatar_vetor(x)}\nIterações: {iteracoes}\nErro: {formatar_numero(erro)}")


def run_mmq() -> None:
    dados = obter_pontos("Dados para mínimos quadrados", EXEMPLOS_PONTOS)
    if dados is None:
        return
    x, y = dados
    maior_grau = len(np.unique(x)) - 1
    if maior_grau < 0:
        raise ValueError("Informe ao menos um ponto.")
    print(f"\nCom esses dados, escolha um grau entre 0 e {maior_grau}.")
    while True:
        grau = ler_int("Grau do polinômio: ", minimo=0)
        if grau <= maior_grau:
            break
        print(f"  [!] Grau incompatível: há {len(np.unique(x))} valores de x distintos; use um grau de 0 a {maior_grau}.")
    coeficientes = ajustar_curva(grau, np.asarray(x), np.asarray(y))
    print(f"\nPolinômio ajustado: P(x) = {formatar_polinomio(coeficientes)}")
    print(f"Coeficientes (maior para menor potência): {formatar_vetor(coeficientes)}")
    plotar_ajuste_mmq(x, y, coeficientes)


def run_interpolacao_definicao() -> None:
    dados = obter_pontos("Pontos para interpolação", EXEMPLOS_PONTOS)
    if dados is None:
        return
    x, y = dados
    coeficientes = definicao(x, y)
    print(f"\nPolinômio interpolador: P(x) = {formatar_polinomio(coeficientes, ordem='crescente')}")
    print(f"Coeficientes (potências crescentes): {formatar_vetor(coeficientes)}")
    plotar_interpolacao_definicao(x, y, coeficientes)


def run_interpolacao_newton() -> None:
    dados = obter_pontos("Pontos para interpolação", EXEMPLOS_PONTOS)
    if dados is None:
        return
    x, y = dados
    coeficientes = diferencas_divididas(x, y)
    print(f"\nPolinômio de Newton: P(x) = {formatar_polinomio_newton(coeficientes, x)}")
    print(f"Coeficientes de diferenças divididas: {formatar_vetor(coeficientes)}")
    print(f"Valor interpolado no ponto médio: {avaliar_newton(x, coeficientes, (min(x) + max(x)) / 2):.8g}")
    plotar_interpolacao_newton(x, y, coeficientes)


def escolher_funcao_integracao():
    exemplos = {
        "f(x) = x² (polinomial)": ("x**2", lambda x: x**2),
        "f(x) = 2x + 1 (linear)": ("2*x + 1", lambda x: 2*x + 1),
        "f(x) = sin(x) (seno)": ("sin(x)", math.sin),
        "f(x) = cos(x) (cosseno)": ("cos(x)", math.cos),
        "f(x) = exp(x) (exponencial)": ("exp(x)", math.exp),
        "f(x) = 1/(1 + x²) (racional)": ("1 / (1 + x**2)", lambda x: 1 / (1 + x**2)),
    }
    dados = escolher_dados("Função a integrar", exemplos)
    if dados is None:
        return None
    if dados == "custom":
        func = ler_funcao("f(x) = ")
        return func, func.expressao
    return dados[1], dados[0]


def run_trapezio() -> None:
    origem = escolher_opcao("Dados para trapézios", ["Integrar uma função", "Usar pontos tabelados"])
    if origem == -1:
        return
    if origem == 0:
        escolha_funcao = escolher_funcao_integracao()
        if escolha_funcao is None:
            return
        func, expressao = escolha_funcao
        a = ler_float("Limite a: ")
        b = ler_float("Limite b: ")
        n = ler_int("Número de subintervalos: ", minimo=1)
        print(f"\nFunção: f(x) = {expressao}\nIntervalo: [{formatar_numero(a)}, {formatar_numero(b)}], n = {n}")
        resultado = trapezio(func, a, b, n)
        print(f"Integral aproximada: {formatar_numero(resultado)}")
        plotar_trapezio(func, a, b, n)
        return
    valores = escolher_dados("Pontos tabelados", exemplos_pontos_integracao())
    if valores == "custom":
        x, y = ler_pontos()
        valores = list(zip(x, y))
    if valores is not None:
        imprimir_pontos([p[0] for p in valores], [p[1] for p in valores])
        resultado = trapezio_tabelado(valores)
        print(f"Integral aproximada: {formatar_numero(resultado)}")
        if len(valores) >= 2:
            plotar_trapezio_tabelado(valores)


def run_simpson() -> None:
    origem = escolher_opcao("Dados para Simpson 1/3", ["Integrar uma função", "Usar pontos tabelados"])
    if origem == -1:
        return
    if origem == 0:
        escolha_funcao = escolher_funcao_integracao()
        if escolha_funcao is None:
            return
        func, expressao = escolha_funcao
        a = ler_float("Limite a: ")
        b = ler_float("Limite b: ")
        while True:
            n = ler_int("Número par de subintervalos: ", minimo=2)
            if n % 2 == 0:
                break
            print("  [!] n deve ser par.")
        print(f"\nFunção: f(x) = {expressao}\nIntervalo: [{formatar_numero(a)}, {formatar_numero(b)}], n = {n}")
        resultado = simpson(func, a, b, n)
        print(f"Integral aproximada: {formatar_numero(resultado)}")
        plotar_simpson(func, a, b, n)
        return
    valores = escolher_dados("Pontos tabelados (espaçamento uniforme)", exemplos_pontos_integracao())
    if valores == "custom":
        x, y = ler_pontos()
        valores = list(zip(x, y))
    if valores is not None:
        imprimir_pontos([p[0] for p in valores], [p[1] for p in valores])
        resultado = simpson_tabelado(valores)
        print(f"Integral aproximada: {formatar_numero(resultado)}")
        plotar_simpson_tabelado(valores)


OPCOES: list[MetodoItem] = [
    MetodoItem("02. Sistemas Lineares", "Eliminação de Gauss", run_eliminacao_gauss),
    MetodoItem("02. Sistemas Lineares", "Fatoração LU", run_fatoracao_lu),
    MetodoItem("02. Sistemas Lineares", "Gauss-Jacobi", run_gauss_jacobi),
    MetodoItem("03. Ajuste de Curvas", "Mínimos Quadrados", run_mmq),
    MetodoItem("04. Interpolação Polinomial", "Definição", run_interpolacao_definicao),
    MetodoItem("04. Interpolação Polinomial", "Polinômio de Newton", run_interpolacao_newton),
    MetodoItem("05. Integração Numérica", "Regra dos Trapézios", run_trapezio),
    MetodoItem("05. Integração Numérica", "1/3 de Simpson", run_simpson),
    MetodoItem("Sistema", "Sair", lambda: None),
]


def _menu_curses(stdscr: curses.window) -> int | None:
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    stdscr.keypad(True)
    idx = 0
    while True:
        stdscr.clear()
        altura, largura = stdscr.getmaxyx()
        titulo = "MÉTODOS NUMÉRICOS"
        subtitulo = "↑/↓ navegar   Enter abrir   q sair"
        # Evita curses.error em terminais estreitos ou com poucas linhas.
        def escrever(y: int, x: int, texto: str, estilo: int = curses.A_NORMAL) -> None:
            if y < 0 or y >= altura or largura <= 1 or x >= largura - 1:
                return
            try:
                stdscr.addnstr(y, x, texto, max(0, largura - x - 1), estilo)
            except curses.error:
                pass

        escrever(0, 2, titulo, curses.A_BOLD)
        escrever(1, 2, subtitulo, curses.A_DIM)
        escrever(2, 2, "─" * max(0, largura - 5), curses.A_DIM)

        # Mostra a categoria junto da opção, sem consumir linhas extras.
        itens_visiveis = max(1, altura - 4)
        inicio = max(0, min(idx - itens_visiveis // 2, len(OPCOES) - itens_visiveis))
        fim = min(len(OPCOES), inicio + itens_visiveis)
        for linha, i in enumerate(range(inicio, fim), start=3):
            item = OPCOES[i]
            marcador = "› " if i == idx else "  "
            texto = f"{marcador}[{item.categoria}] {item.nome}"
            estilo = curses.A_REVERSE | curses.A_BOLD if i == idx else curses.A_NORMAL
            escrever(linha, 3, texto, estilo)
        escrever(altura - 1, 2, f"{idx + 1}/{len(OPCOES)}", curses.A_DIM)
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
            print("\n=== MÉTODOS NUMÉRICOS ===")
            categoria_atual = None
            for i, item in enumerate(OPCOES, start=1):
                if item.categoria != categoria_atual:
                    categoria_atual = item.categoria
                    print(f"\n{categoria_atual}")
                print(f"  {i:>2}) {item.nome}")
            print("\n  0) Sair")
            escolha = ler_int("Selecione uma opção: ", minimo=0)
            while escolha > len(OPCOES):
                print(f"  [!] Escolha um número entre 0 e {len(OPCOES)}.")
                escolha = ler_int("Selecione uma opção: ", minimo=0)
            selecionado = None if escolha == 0 else escolha - 1

        if selecionado is None or OPCOES[selecionado].nome == "Sair":
            print("Saindo...")
            break

        print("\033[2J\033[H", end="")
        print(f"=== {OPCOES[selecionado].nome.upper()} ===\n")
        while True:
            try:
                OPCOES[selecionado].acao()
                break
            except KeyboardInterrupt:
                print("\n[!] Operação cancelada.")
                break
            except Exception as erro:
                print(f"\n[!] Erro nos dados: {erro}")
                print("Digite os dados novamente. Pressione Ctrl+C para cancelar.")
        input("\nPressione ENTER para voltar ao menu...")


if __name__ == "__main__":
    main()
