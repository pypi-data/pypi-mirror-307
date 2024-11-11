#include "params/p_idm.h"

p_idm::p_idm(){
}

p_idm::p_idm(double v0, double T, double a, double b, double s0, double l) {
	if (v0 < 0 || T <= 0) throw Exception(901, "Wrong parameters.");
	this->v0 = v0;
	this->T = T;
	this->a = a;
	this->b = b;
	this->s0 = s0;
	this->l = l;
}
