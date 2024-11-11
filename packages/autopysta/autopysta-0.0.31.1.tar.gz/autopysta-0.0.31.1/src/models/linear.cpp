#include <math.h>
#include <random>
#include "models/linear.h" 

linear::linear() {
	pars = new p_linear();
}

linear::linear(p_linear* p) {
	pars = p;
}

double linear::accel(Point* leader, Point* follower, params* q) {
	p_linear* p = (p_linear*)PICK(q, pars);
    double V = p->V;
    double c1 = p->c1;
    double sr = p->sr;
    double tau = p->tau;
    double c3 = p->c3;

	double fa = (V - follower->V()) * c1;
	if (leader == nullptr) {
		return fa;
	}

    double fr = (leader->V() - follower->V()) * p->c2 + (leader->X() - follower->X() - sr - follower->V() * tau) * c3;
	if (fr > 0) fr = 0;

    return fa + fr;
}


double linear::equil_spcg(double /* vl */, double vf, params* q) {
	p_linear* p = (p_linear*)PICK(q, pars);
    double V = p->V;
    double c1 = p->c1;
    double sr = p->sr;
    double tau = p->tau;
    double c3 = p->c3;
    return sr - V * c1 / c3 + (tau + c1 / c3) * vf;
}

double linear::wave_speed(Point* /* leader */, Point* /* follower */, params* q) {
	p_linear* p = (p_linear*)PICK(q, pars);
    double V = p->V;
    double c1 = p->c1;
    double sr = p->sr;
    double tau = p->tau;
    double c3 = p->c3;
    return (sr * c3 - V * c1) / (c1 + c3 * tau);
}

double linear::free_flow_speed(params* q) {
	p_linear* p = (p_linear*)PICK(q, pars);
	return p->V;
}
