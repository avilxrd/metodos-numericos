#include "funcoes.h"

#include <iostream>
#include <string>
#include <iomanip>
#include <cstdlib>

using namespace std;

const std::string YELLOW = "\033[33m";
const std::string RESET  = "\033[0m";

void exibirFuncoes() {
    cout << YELLOW << "opcoes de funcoes:" << RESET << "\n"
         << "[1] f(x) = 4*cos(x) - exp(2*x)\n"
         << "[2] f(x) = (x/2) - tan(x)\n"
         << "[3] f(x) = 1 - x*ln(x)\n"
         << "[4] f(x) = 2^x - 3*x\n"
         << "[5] f(x) = x^3 + x - 10\n"
         << "[0] sair\n" << endl;
}

void exibirMetodos() {
    cout << YELLOW << "opcoes de metodos:" << RESET << "\n"
         << "[1] Bissecao\n"
         << "[2] Falsa Posicao\n"
         << "[3] Newton-Raphson\n"
         << "[4] Secantes\n"
         << "[0] voltar ao menu anterior\n" << endl;
}

std::function<double(double)> getFuncao(int id) {
    switch (id) {
        case 1: return funcao_a;
        case 2: return funcao_b;
        case 3: return funcao_c;
        case 4: return funcao_d;
        case 5: return funcao_e;
        default: return nullptr;
    }
}

void limparTela() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

int main()
{
    int op_funcao, op_metodo;

    while (true) {
        exibirFuncoes();
        cout << "escolha uma funcao: ";
        if (!(cin >> op_funcao) || op_funcao == 0) break;

        auto func = getFuncao(op_funcao);
        if (func == nullptr) {
            limparTela();
            cout << "funcao invalida!\n" << endl;
            continue;
        }

        while (true) {
            limparTela();
            exibirMetodos();
            cout << "escolha um metodo: ";
            if (!(cin >> op_metodo) || op_metodo == 0) {
                limparTela();
                break;
            }

            double a, b, x0, res;
            double prec_e1 = BASE_PRECISION, prec_e2 = BASE_PRECISION;

            limparTela();

            switch (op_metodo) {
                case 1:
                    cout << "digite o intervalo [a b]: ";
                    cin >> a >> b;
                    limparTela();
                    res = bissecao(func, a, b, prec_e1);
                    break;

                case 2:
                    cout << "digite o intervalo [a b]: ";
                    cin >> a >> b;
                    limparTela();
                    res = falsaPosicao(func, a, b, prec_e1, prec_e2);
                    break;

                case 3:
                    cout << "digite o ponto inicial x0: ";
                    cin >> x0;
                    limparTela();
                    res = newtonRaphson(func, x0, prec_e1, prec_e2);
                    break;

                case 4:
                    cout << "digite as aproximacoes iniciais [a b]: ";
                    cin >> a >> b;
                    limparTela();
                    res = secantes(func, a, b, prec_e1, prec_e2);
                    break;

                default:
                    cout << "metodo invalido!" << endl;
                    continue;
            }

            cout << endl << fixed << setprecision(14);
            cout << "resultado encontrado: " << res << endl << endl;

            cout << YELLOW << "pressione enter para continuar..." << RESET;
            cin.ignore();
            cin.get();
        }
    }

    return 0;
}