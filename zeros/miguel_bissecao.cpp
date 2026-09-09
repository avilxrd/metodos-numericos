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


double bissec(double a, double b, double precision_e)
{
    //retorna um nan caso nao satisfaca o teorema de bolzano
    if (satisfyBolzano(a,b) == 0) { return nan(""); }
    
    int counter=1;
    double medio, fm;

    cout << "\n" << string(68, '-') << endl;
    cout << left 
         << setw(5)  << "i"
         << setw(12) << "a"
         << setw(12) << "b"
         << setw(12) << "m"
         << setw(14) << "f(m)"
         << setw(12) << "|b - a|" 
         << endl;
    cout << string(68, '-') << endl;

    do
    {
        medio = (a+b)/2.0;
        double fm = func(medio);

        //mostra uma tabela com os dados de cada iteracao
        cout << left 
             << setw(5)  << counter
             << setw(12) << fixed << setprecision(6) << a
             << setw(12) << fixed << setprecision(6) << b
             << setw(12) << fixed << setprecision(6) << medio
             << setw(14) << scientific << setprecision(3) << fm
             << setw(12) << fixed << setprecision(6) << std::abs(b - a)
             << endl;

        //verifica a parada do algoritmo
        // (sol. por dominio)       || (sol. por imagem)       || (estourou lim. de iterações)
        if ( (std::abs(b-a) <= precision_e) || (std::abs(fm) < precision_e) || (counter > MAX_ITERS) ) { break; }

        if ( satisfyBolzano(a, medio) == 1 ) { b = medio; }
        else { a = medio; }

        counter++;
    } while (1);

    cout << "iters: " << counter << endl;
    return medio;
}


int main()
{
    cout << "tentando aproximar a funcao pelo metodo da bissecao com e = " << BASE_PRECISION << endl;
    double res = bissec(0, 1, BASE_PRECISION);
    
    if (isnan(res)) {
        cout << "intervalo invalido";
        return -1;
    }
    
    cout<<fixed<<setprecision(14);
    cout<<endl<<"aproxim: " << res << endl;
    return 0;
}
