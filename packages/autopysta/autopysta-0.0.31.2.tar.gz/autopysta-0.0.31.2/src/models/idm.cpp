#include "models/idm.h"
#include <math.h>
#include <algorithm>


idm::idm(){
	pars = new p_idm();
}

idm::idm(p_idm * pars)
{
	this->pars = pars;
}

double idm::accel(Point* leader, Point* follower, params* q){
	p_idm* p = (p_idm *)PICK(q, pars);
	if (p->v0 == 0) throw Exception(902, "Division by zero.");
	double ff = 1 - pow(follower->V() / p->v0, p->dl);
	
	if (leader != nullptr) {
		if (p->a * p->b == 0) throw Exception(902, "Division by zero.");
		double si = desired_minimum_gap(leader->V(), follower->V(), p);

		if (leader->X() - follower->X() - p->l == 0) throw Exception(902, "Division by zero.");
		
		return p->a*(ff - pow(si / (leader->X() - follower->X() - p->l), 2));
	}
	else return p->a*ff;
}

double idm::desired_minimum_gap(double vl, double vf, params* q) {
	p_idm* p = (p_idm*)PICK(q, pars);
	double var = sqrt(p->a * p->b);
	double delta_v = vf - vl;
	if (var == 0) throw Exception(902, "Division by zero.");
	return p->s0 + std::max(0.0, p->T * vf + (vf*delta_v) / (2 * var));
}

double idm::equil_spcg(double vl, double vf, params* q) {
	p_idm* p = (p_idm*)PICK(q, pars);
	//The length of the vehicle is added to convert the gap to spacing
	return desired_minimum_gap(vl, vf, p) + p->l;
}

double idm::wave_speed(Point* /* leader */, Point* /* follower */, params* /* p */){

	return 0.0;
}

double idm::free_flow_speed(params * q)
{
	p_idm *p = (p_idm*)PICK(q, pars);
	return p->v0;
}
