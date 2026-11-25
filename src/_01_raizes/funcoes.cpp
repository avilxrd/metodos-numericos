#include "funcoes.h"

#include <cmath>
#include <iomanip>
#include <iostream>
#include <functional>

using namespace std;

//funcoes de teste/exemplo
double funcao_a(double x)
{
    return 4.0 * std::cos(x) - std::exp(2.0 * x);
}

double funcao_b(double x)
{
    return (x / 2.0) - std::tan(x);
}

double funcao_c(double x)
{
    return 1.0 - x * std::log(x);
}

double funcao_d(double x)
{
    return std::pow(2.0, x) - 3.0 * x;
}

double funcao_e(double x)
{
    return std::pow(x, 3.0) + x - 10.0;
}

//funcoes auxiliares
bool satisfyBolzano(const std::function<double(double)>& f, double a, double b)
{
    if ( (f(a) * f(b)) < 0 ) { return true; }
    return false;
}

double derivative(const std::function<double(double)>& f, double x, double h)
{
    return (f(x + h) - f(x - h)) / (2.0 * h);
}

static bool isValid(double v)
{
    return !std::isnan(v) && !std::isinf(v);
}

// metodos numericos para zeros de funcoes
double bissecao(const std::function<double(double)>& f, double a, double b, double precision)
{
    if (!isValid(a) || !isValid(b) || !isValid(precision) || precision <= 0 || a > b) {
        return nan("");
    }

    double fa = f(a);
    double fb = f(b);

    if (!isValid(fa) || !isValid(fb)) return nan("");

    if (std::abs(fa) < precision) return a;
    if (std::abs(fb) < precision) return b;

    if ((fa > 0) == (fb > 0))
    {
        return nan("");
    }

    int counter = 1;
    double medio; 

    cout << "\n--- METODO DA BISSECAO ---" << endl;
    cout << string(90, '-') << endl;
    cout << left 
         << setw(5)  << "i"
         << setw(20) << "a"
         << setw(20) << "b"
         << setw(20) << "m"
         << setw(25) << "f(m)"
         << endl;
    cout << string(90, '-') << endl;

    do
    {
        medio = (a+b)/2.0;
        double fm = f(medio);

        //mostra uma tabela com os dados de cada iteracao
        cout << left 
             << setw(5)  << counter
             << setw(20) << fixed << setprecision(14) << a
             << setw(20) << fixed << setprecision(14) << b
             << setw(20) << fixed << setprecision(14) << medio
             << setw(25) << scientific << setprecision(14) << fm
             << endl;

        //verifica a parada do algoritmo
        if (!isValid(fm)) return nan("");
        if (std::abs(fm) < precision) return medio;
        if (std::abs(b - a) <= precision) return medio;
        if (counter >= MAX_ITERS) return nan("");

        if ((fa > 0) != (fm > 0)) {
            b = medio;
            fb = fm;
        } else {
            a = medio;
            fa = fm;
        }

        counter++;
    } while (1);

    return medio;
}

double falsaPosicao(const std::function<double(double)>& f, double a, double b, double precision_e1, double precision_e2)
{
    if (!isValid(a) || !isValid(b) || !isValid(precision_e1) || !isValid(precision_e2) ||
        precision_e1 <= 0 || precision_e2 <= 0 || a > b) {
        return nan("");
    }

    double fa = f(a);
    double fb = f(b);

    if (!isValid(fa) || !isValid(fb)) return nan("");
    if (std::abs(fa) < precision_e2) return a;
    if (std::abs(fb) < precision_e2) return b;
    if ((fa > 0) == (fb > 0)) return nan("");

    int counter = 1;
    double x = nan("");

    cout << "\n--- METODO DA FALSA POSICAO ---" << endl;
    cout << string(90, '-') << endl;
    cout << left 
         << setw(5)  << "i"
         << setw(20) << "a"
         << setw(20) << "b"
         << setw(20) << "x"
         << setw(25) << "f(x)"
         << endl;
    cout << string(90, '-') << endl;
    do
    {
        double denominador = fb - fa;
        if (!isValid(denominador) || std::abs(denominador) < 1e-15) return nan("");

        x = (a * fb - b * fa) / denominador;
        double fx = f(x);

        if (!isValid(x) || !isValid(fx))
        {
            cerr << "nao convergiu" << endl;
            return nan("");
        }
        
        cout << left 
             << setw(5)  << counter
             << setw(20) << fixed << setprecision(14) << a
             << setw(20) << fixed << setprecision(14) << b
             << setw(20) << fixed << setprecision(14) << x
             << setw(25) << scientific << setprecision(14) << fx
             << endl;

        if (std::abs(fx) < precision_e2) return x;

        if ((fa > 0) != (fx > 0)) {
            b = x;
            fb = fx;
        } else {
            a = x;
            fa = fx;
        }

        if (std::abs(a - b) < precision_e1) return (a + b) / 2.0;
        if (counter >= MAX_ITERS) return nan("");
        counter++;
    } while (1);
}

double newtonRaphson(const std::function<double(double)>& f, double x0, double precision_e1, double precision_e2)
{
    if (!isValid(x0) || !isValid(precision_e1) || !isValid(precision_e2) ||
        precision_e1 <= 0 || precision_e2 <= 0) {
        return nan("");
    }

    double x = nan("");
    double fx0 = f(x0);

    if (!isValid(fx0)) return nan("");

    cout << "\n--- METODO DE NEWTON-RAPHSON ---" << endl;
    cout << string(90, '-') << endl;
    cout << left 
         << setw(5)  << "i"
         << setw(20) << "x0"
         << setw(20) << "x1"
         << setw(20) << "f'(x0)"
         << setw(25) << "f(x1)"
         << endl;
    cout << string(90, '-') << endl;
    
    if (std::abs(fx0) < precision_e1) { return x0; }

    int counter = 1;
    while (1)
    {
        double fx0_d = derivative(f, x0);

        if (!isValid(fx0_d) || std::abs(fx0_d) < 1e-12)
        {
            cerr << "derivada nula ou proxima de zero" << endl;
            return x;
        }
        
        x = x0 - fx0/fx0_d;
        double fx = f(x);

        if (std::isnan(x) || std::isnan(fx) || std::isinf(x) || std::isinf(fx))
        {
            cerr << "iteracao saiu do dominio da funcao" << endl;
            return nan("");
        }

        cout << left 
             << setw(5)  << counter
             << setw(20) << fixed << setprecision(14) << x0
             << setw(20) << fixed << setprecision(14) << x
             << setw(20) << fixed << setprecision(14) << fx0_d
             << setw(25) << scientific << setprecision(14) << fx
             << endl;

        if (std::abs(fx) < precision_e1) return x;
        if (std::abs(x - x0) < precision_e2) return nan("");
        if (counter >= MAX_ITERS) return nan("");
        x0  = x;
        fx0 = fx;
        counter++;
    }
}

double secantes(const std::function<double(double)>& f, double a, double b, double precision_e1, double precision_e2)
{
    if (!isValid(a) || !isValid(b) || !isValid(precision_e1) || !isValid(precision_e2) ||
        precision_e1 <= 0 || precision_e2 <= 0) {
        return nan("");
    }

    double fa = f(a);
    double fb = f(b);

    if (!isValid(fa) || !isValid(fb)) return nan("");
    if (std::abs(fa) < precision_e1) return a;
    if (std::abs(fb) < precision_e1) return b;
    if (std::abs(b - a) < precision_e2) return nan("");
    
    int counter = 1;
    double x = b;

    cout << "\n--- METODO DAS SECANTES ---" << endl;
    cout << string(90, '-') << endl;
    cout << left 
         << setw(5)  << "i"
         << setw(20) << "x0 (a)"
         << setw(20) << "x1 (b)"
         << setw(20) << "x2 (novo)"
         << setw(25) << "f(x2)"
         << endl;
    cout << string(90, '-') << endl;

    while(true)
    {
        double denominador = fb - fa;
        if (!isValid(denominador) || std::abs(denominador) < 1e-15) return nan("");

        x = b - (fb / denominador) * (b - a);
        double fx = f(x);

        if (!isValid(x) || !isValid(fx))
        {
            cerr << "iteracao saiu do dominio da funcao" << endl;
            return nan("");
        }

        cout << left 
             << setw(5)  << counter
             << setw(20) << fixed << setprecision(14) << a
             << setw(20) << fixed << setprecision(14) << b
             << setw(20) << fixed << setprecision(14) << x
             << setw(25) << scientific << setprecision(14) << fx
             << endl;

        if (std::abs(fx) < precision_e1) return x;
        if (std::abs(x - b) < precision_e2) return nan("");

        a = b;
        fa = fb;

        b = x;
        fb = fx;
        if (counter >= MAX_ITERS) return nan("");
        counter++;
    }
}

