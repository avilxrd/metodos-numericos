#include <iostream>
#include <cmath>
#include <iomanip>


double func(double x){
    return x*x*x -2;
}


int satisfyBolzano(double a, double b){
    if ( 
        (func(a) < 0 and func(b) > 0) or 
        (func(a) > 0 and func(b) < 0)
    ) { return 1; } // true
    
    return 0; // false
}


const double e = 1e-15;
double bissec(double a, double b){
    double k;
    double m=0;
    double fa, fb, fm;
    double x; // x = b-a

    if ( satisfyBolzano(a, b) == 0 ) { return std::nan(""); }

    m = (a+b)/2;
    do {
        k = m;
        x = b-a;
        
        if (satisfyBolzano(a,m) == 1) { b = m; }
        else if (satisfyBolzano(b,m) == 1) { a = m; }
        m = (a+b)/2;
    } while ( (std::abs(m-k) >= e) or (std::abs(func(m)) >= e) );
    
    return m;
}


int main()
{
    std::cout << "tentando aproximar a funcao pelo metodo da bissecao com e = " << e << std::endl;
    double res = bissec(0,2);
    
    if (std::isnan(res)) {
        std::cout << "intervalo invalido";
        return -1;
    }
    
    std::cout<<std::fixed<<std::setprecision(14);
    std::cout<<std::endl<<"aproxim: " << res;
    return 0;
}
