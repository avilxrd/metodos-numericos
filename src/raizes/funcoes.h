#ifndef FUNCOES_H
#define FUNCOES_H

#include <functional>

#define BASE_PRECISION 1e-10
#define MAX_ITERS 1000

//funcoes de teste para os codigos
double funcao_a(double x);
double funcao_b(double x);
double funcao_c(double x);
double funcao_d(double x);
double funcao_e(double x);

//funcoes auxiliares
bool satisfyBolzano(const std::function<double(double)>& f, double a, double b);
double derivative(const std::function<double(double)>& f, double x, double h = BASE_PRECISION);
static bool isValid(double v);

//metodos de zeros reais de funcoes reais
double bissecao(const std::function<double(double)>& f, double a, double b, double precision=BASE_PRECISION);
double falsaPosicao(const std::function<double(double)>& f, double a, double b, double precision_e1=BASE_PRECISION, double precision_e2=BASE_PRECISION);
double newtonRaphson(const std::function<double(double)>& f, double x0, double precision_e1=BASE_PRECISION, double precision_e2=BASE_PRECISION);
double secantes(const std::function<double(double)>& f, double a, double b, double precision_e1=BASE_PRECISION, double precision_e2=BASE_PRECISION);

#endif // FUNCOES_H