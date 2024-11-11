#include "params/p_linear.h"

p_linear::p_linear()
{
}


p_linear::p_linear(double V, double c1, double c2, double c3, double sr, double tau)
{
	this->V = V;
	this->c1 = c1;
	this->c2 = c2;
	this->c3 = c3;
	this->sr = sr;
	this->tau = tau;
}

/*p_linear::p_linear(){
	this->V = 120/3.6;
	this->c1 = 3.0/40.0;
	this->c2 = 93.0/160.0;
	this->c3 = 9.0/64.0;
	this->sr = 220.0/9;
	this->tau = 2.0/3;
}*/
