#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

#define MAX_ITERS 1000
#define BASE_PRECISION 1e-3


double func(double x){
    return x*x*x -9*x + 3;
}


int satisfyBolzano(double a, double b)
{
    if (func(a)*func(b) < 0) { return 1; }
    return 0;
}


double falsaPosicao(double a, double b, double precision_e1, double precision_e2)
{
    double fa = func(a);
    double fb = func(b);

    if ( std::abs(a-b) < precision_e1 )
    {
        if ( std::abs(fa) < precision_e2 ) { return a; }
        else { return b; }
    }

    int counter = 1;
    double x;

    cout << "\n" << string(68, '-') << endl;
    cout << left 
         << setw(5)  << "i"
         << setw(12) << "m"
         << setw(14) << "f(m)"
         << setw(12) << "|b - a|" 
         << endl;
    cout << string(68, '-') << endl;
    do
    {
        double fa = func(a);
        double fb = func(b);
    
        x = (a*fb - b*fa)/(fb-fa);
        double fx = func(x);
        
        cout << left 
             << setw(5)  << counter
             << setw(12) << fixed << setprecision(6) << x
             << setw(14) << scientific << setprecision(3) << fx
             << setw(12) << fixed << setprecision(6) << std::abs(b - a)
             << endl;

        if (std::abs(fx) < precision_e2) { break; }

        if ( satisfyBolzano(a, x) ) { b = x; }
        else { a = x; }

        if (std::abs(a-b) < precision_e1) { break; }
        counter++;
    } while (1);

    return x;
}

int main()
{
    cout << "tentando aproximar a funcao pelo metodo da bissecao com e = " << BASE_PRECISION << endl;
    double res = falsaPosicao(0, 1, BASE_PRECISION, BASE_PRECISION);
    
    if (isnan(res)) {
        cout << "intervalo invalido";
        return -1;
    }
    
    cout<<fixed<<setprecision(14);
    cout<<endl<<"aproxim: " << res << endl;
    return 0;
}
