# Correções pendentes

Lista conferida contra o estado atual dos arquivos. Foram removidos os itens marcados como corrigidos que realmente não aparecem mais como problemas. Os itens abaixo ainda precisam de atenção.

## Raízes de funções (C++)

Arquivo: `src/_01_raizes/funcoes.cpp`

### Bisseção

- Tratar `f(a) == 0` e `f(b) == 0` antes de exigir mudança de sinal. `satisfyBolzano()` aceita apenas produto estritamente negativo, então rejeita raiz exatamente na extremidade.
- Validar que a tolerância seja positiva e que os valores da função sejam finitos.
- Informar explicitamente a não convergência ao atingir o limite de iterações.

### Falsa posição

- Verificar se uma extremidade é raiz ou se o intervalo contém mudança de sinal. Atualmente o método pode iterar em intervalo que não delimita uma raiz.
- Se `f(a)` e `f(b)` forem quase iguais, informar falha em vez de retornar `x`, que pode ainda ser `NaN`.
- Validar tolerâncias positivas e valores finitos.
- Distinguir convergência de encerramento por limite de iterações.

### Newton-Raphson

- Validar tolerâncias positivas e valores finitos.
- Distinguir convergência do encerramento por `MAX_ITERS`; atualmente retorna a última aproximação mesmo sem atingir a tolerância.
- Documentar a limitação da derivada numérica por diferenças finitas ou permitir controlar seu passo.

### Secantes

- Quando `f(b) - f(a)` é quase zero, informar falha em vez de interromper e retornar a aproximação atual.
- Distinguir convergência do encerramento por limite de iterações ou saída do domínio.
- Validar tolerâncias positivas e valores finitos.
- Se `abs(b-a) < precision_e2`, verificar também o resíduo `abs(f(b))` antes de retornar `b` como solução.

## Sistemas lineares

### Eliminação de Gauss

Arquivo: `src/_02_sistemas_lineares/eliminacao_gauss.py`

- Validar matriz não vazia e entradas finitas. Uma matriz vazia chega ao acesso `A[-1, -1]` e causa erro de índice.
- Validar também matriz não vazia e dados finitos em `retrossubstituicao()`.

### Fatoração LU

Arquivo: `src/_02_sistemas_lineares/fatoracao_lu.py`

- Corrigir `np.iscloes` para `np.isclose` nas duas rotinas de substituição; o nome atual não existe no NumPy e causa erro ao executar.
- Os nomes das funções ainda estão trocados em relação aos sistemas que resolvem: `substituicao_regressiva()` resolve o triangular inferior (substituição para frente), enquanto `substituicao_progressiva()` resolve o superior (substituição para trás). Renomear funções ou corrigir os nomes/comentários.
- Validar dimensão e formato de `b` antes de calcular `P @ b`.
- Validar matriz não vazia e entradas finitas.

### Gauss-Jacobi

Arquivo atual: `src/_02_sistemas_lineares/gauss_jacobi.py`

- Diagonal sem zeros não garante convergência. Documentar ou verificar uma condição suficiente, como dominância diagonal estrita.
- Validar valores finitos em `A`, `b` e `x_inicial`.
- Validar que `max_iters >= 1`. A tolerância positiva já é verificada, e a mensagem ao atingir o limite de iterações já foi adicionada.

## Ajuste de curvas

### Mínimos quadrados polinomiais (MMQ)

Arquivo: `src/_03_ajuste_curvas/mmq.py`

- Validar que `xi` e `fxi` tenham mesmo tamanho, não estejam vazios e que o grau seja válido para a quantidade de dados.
- As operações `xi ** expoente` e `fxi * (...)` esperam arrays NumPy, mas os argumentos estão anotados como listas e não são convertidos dentro das funções. Converter as entradas ou ajustar/documentar a interface.
- As equações normais podem ficar mal condicionadas para dados ou graus maiores; documentar essa limitação ou considerar uma solução por QR.

## Interpolação polinomial

### Método por definição (Vandermonde)

Arquivo: `src/_04_interpolacao/definicao.py`

- Corrigir a ordem dos coeficientes usada no gráfico: a matriz tem colunas `1, x, x², ...`, então `gauss()` devolve coeficientes em ordem crescente, mas `np.polyval()` espera ordem decrescente. Inverter os coeficientes ao plotar ou montar a matriz em ordem decrescente.
- Validar que `x` e `y` tenham mesmo tamanho, sejam vetores não vazios e que os valores de `x` sejam distintos.

### Polinômio de Newton

Arquivo: `src/_04_interpolacao/newton.py`

- Validar vetores vazios e dimensões unidimensionais.
- Validar entradas de `avaliar_newton()` quando chamada diretamente, incluindo coeficientes não vazios e tamanhos compatíveis com os pontos.
- Considerar validar que os dados sejam finitos.

## Integração numérica

### Regra dos trapézios

Arquivo: `src/_05_integracao_numerica/trapezio.py`

- Na versão tabelada, validar formato dos pontos, ordem e valores finitos. Espaçamento desigual é permitido.

### Regra 1/3 de Simpson

Arquivo: `src/_05_integracao_numerica/simpson.py`

- Garantir que `n` seja inteiro par maior ou igual a 2; a validação atual não rejeita necessariamente valores não inteiros.
- Na versão tabelada, validar formato de cada ponto e valores finitos. As verificações de quantidade ímpar, ordem crescente e espaçamento uniforme já existem.

## Integração com o menu

Arquivo: `main.py`

- Várias opções ainda não estão ligadas aos métodos correspondentes. As opções de raízes e LU exibem `[TODO]`, e outras apontam para `run_fatoracao_lu`, que também é provisório.
- Conectar as opções aos métodos implementados ou indicar claramente no menu quais ainda não estão disponíveis.
- Alinhar o README com o estado real da interface: nem todos os métodos marcados como concluídos podem ser executados pelo menu.
