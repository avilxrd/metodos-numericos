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


double derivative(const std::function<double(double)>& func, double x, double h = BASE_PRECISION) {
    return (func(x + h) - func(x - h)) / (2.0 * h);
}


double newtonRaphson(double x0, double precision_e1, double precision_e2)
{
    double x = nan("");
    double fx0 = func(x0);
    if (std::abs(fx0) < precision_e1) { return x0; }

    while (1)
    {
        double fx0_d = derivative(func, x0);

        if (std::abs(fx0_d) < 1e-12) 
        {
            cerr << "derivada nula ou proxima de zero" << endl;
            return x;
        }
        
        x = x0 - fx0/fx0_d;
        cout << x << endl;
        double fx = func(x);

        if (std::abs(fx) < precision_e1 || std::abs(x - x0) < precision_e2) { break; }
        x0  = x;
        fx0 = fx;
    }
    
    return x;
}



int main()
{
    cout << "tentando aproximar a funcao pelo metodo de newton-raphson com e = " << BASE_PRECISION << endl;
    double res = newtonRaphson(1, BASE_PRECISION, BASE_PRECISION);
    
    if (isnan(res)) {
        cout << "intervalo invalido";
        return -1;
    }
    
    cout<<fixed<<setprecision(14);
    cout<<endl<<"aproxim: " << res << endl;
    return 0;
}
