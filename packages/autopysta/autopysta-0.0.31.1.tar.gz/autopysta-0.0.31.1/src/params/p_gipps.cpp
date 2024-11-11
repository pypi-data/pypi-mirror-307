#include "params/p_gipps.h"

p_gipps::p_gipps(){
}

p_gipps::p_gipps(double an, double bn, double sn, double vn, double tau, double bg)
{
	this->an = an;
	this->bn = bn;
	this->sn = sn;
	this->vn = vn;
	this->tau = tau;
	this->bg = bg;
}
