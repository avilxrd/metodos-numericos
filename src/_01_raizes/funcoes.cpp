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
    //retorna um nan caso nao satisfaca o teorema de bolzano
    if (satisfyBolzano(f, a, b) == false) { return nan(""); }

    int counter=1;
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
        if ( (std::abs(b-a) <= precision) || (std::abs(fm) < precision) ) { break; }
        if (counter > MAX_ITERS) { return nan(""); }

        if ( satisfyBolzano(f, a, medio) == 1 ) { b = medio; }
        else { a = medio; }

        counter++;
    } while (1);

    return medio;
}

double falsaPosicao(const std::function<double(double)>& f, double a, double b, double precision_e1, double precision_e2)
{
    double fa = f(a);
    double fb = f(b);

    if ( std::abs(a-b) < precision_e1 )
    {
        if ( std::abs(fa) < precision_e2 ) { return a; }
        else { return b; }
    }

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
        double fa = f(a);
        double fb = f(b);

        if ( std::abs(fb - fa) < 1e-15 ) { break; }

        x = (a*fb - b*fa)/(fb-fa);
        double fx = f(x);

        if (std::isnan(x) || std::isnan(fx) || std::isinf(x) || std::isinf(fx))
        {
            cerr << "nao convergiu" << endl;
            x = nan("");
            break;
        }
        
        cout << left 
             << setw(5)  << counter
             << setw(20) << fixed << setprecision(14) << a
             << setw(20) << fixed << setprecision(14) << b
             << setw(20) << fixed << setprecision(14) << x
             << setw(25) << scientific << setprecision(14) << fx
             << endl;

        if (std::abs(fx) < precision_e2) { break; }

        if ( satisfyBolzano(f, a, x) ) { b = x; }
        else { a = x; }

        if (std::abs(a-b) < precision_e1) { break; }
        if (counter >= MAX_ITERS) { break; }
        counter++;
    } while (1);

    return x;
}

double newtonRaphson(const std::function<double(double)>& f, double x0, double precision_e1, double precision_e2)
{
    double x = nan("");
    double fx0 = f(x0);

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

        if (std::abs(fx0_d) < 1e-12) 
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

        if (std::abs(fx) < precision_e1 || std::abs(x - x0) < precision_e2) { break; }
        if (counter >= MAX_ITERS) { break; }
        x0  = x;
        fx0 = fx;
        counter++;
    }
    return x;
}

double secantes(const std::function<double(double)>& f, double a, double b, double precision_e1, double precision_e2)
{
    double fa = f(a);
    double fb = f(b);

    if ( std::abs(fa) < precision_e1 ){ return a; }
    if ( std::abs(fb) < precision_e1 || std::abs(b - a) < precision_e2 ){ return b; }
    
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
        if ( std::abs(fb - fa) < 1e-15 ) { break; }

        x  = b - ( (fb / (fb - fa)) * (b - a) );
        double fx = f(x);

        if (std::isnan(x) || std::isnan(fx) || std::isinf(x) || std::isinf(fx))
        {
            cerr << "iteracao saiu do dominio da funcao" << endl;
            break;
        }

        cout << left 
             << setw(5)  << counter
             << setw(20) << fixed << setprecision(14) << a
             << setw(20) << fixed << setprecision(14) << b
             << setw(20) << fixed << setprecision(14) << x
             << setw(25) << scientific << setprecision(14) << fx
             << endl;

        if ( std::abs(fx) < precision_e1 ||  std::abs(x - b) < precision_e2) { break; };

        a = b;
        fa = fb;

        b = x;
        fb = fx;
        if (counter >= MAX_ITERS) { break; }
        counter++;
    }
    return x;
}

