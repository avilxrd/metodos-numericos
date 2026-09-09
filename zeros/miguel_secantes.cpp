#include <iostream>
#include <cmath>
#include <iomanip>
#include <functional>

using namespace std;

#define MAX_ITERS 1000
#define BASE_PRECISION 1e-3


double func(double x){
    return x*x*x -9*x + 3;
}


double secantes(double ponto_a, double ponto_b, double precision_e1, double precision_e2)
{
    double fa = func(ponto_a);
    double fb = func(ponto_b);

    if ( std::abs(fa) < precision_e1 ){ return ponto_a; }
    if ( std::abs(fb) < precision_e1 || std::abs(ponto_b - ponto_a) < precision_e2 ){ return ponto_b; }
    
    double x = ponto_b;
    while(true)
    {
        x  = ponto_b - ( (fb / (fb - fa)) * (ponto_b - ponto_a) );
        double fx = func(x);

        if ( std::abs(fx) < precision_e1 ||  std::abs(x - ponto_b) < precision_e2) { break; };

        ponto_a = ponto_b;
        fa = fb;

        ponto_b = x;
        fb = fx;
    }

    return x;
}



int main()
{
    cout << "tentando aproximar a funcao pelo metodo de newton-raphson com e = " << BASE_PRECISION << endl;
    double res = secantes(0, 1, BASE_PRECISION, BASE_PRECISION);
    
    if (isnan(res)) {
        cout << "intervalo invalido";
        return -1;
    }
    
    cout<<fixed<<setprecision(14);
    cout<<endl<<"aproxim: " << res << endl;
    return 0;
}
