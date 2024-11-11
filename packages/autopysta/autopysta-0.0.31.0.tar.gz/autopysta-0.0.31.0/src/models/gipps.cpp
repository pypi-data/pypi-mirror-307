#include "models/gipps.h"


gipps::gipps() {
	pars = new p_gipps();
}

gipps::gipps(p_gipps* p) {
	pars = p;
}

void gipps::validate_parameters(params* p) {
	p_gipps* q = (p_gipps*)PICK(p, pars);
	if (q->vn == 0 || q->bg == 0 || q->tau == 0 || q->bn == 0) throw Exception(902, "Division by zero");
}

double gipps::accel(Point* leader, Point* follower, params* q) {
	p_gipps* p = (p_gipps*)PICK(q, pars);
	double dv;
	double vnfl = follower->V() + 2.5*p->an*p->tau * (1 - (follower->V()/p->vn)) * std::sqrt(0.025 + (follower->V()/p->vn));

	if (leader != nullptr) {
        double vncg = p->bn*p->tau + std::sqrt(std::pow(p->bn, 2) * std::pow(p->tau, 2) - p->bn*(2 * (leader->X() - p->sn - follower->X()) - (follower->V() * p->tau) - (std::pow(leader->V(), 2) / p->bg)));

		if (std::isnan(vncg) || vncg < 0) vncg = 0;
		dv = (vnfl < vncg ? vnfl : vncg) - follower->V();
    }
    else {
        dv = vnfl - follower->V();
    }

    return dv/p->tau;
}

double gipps::equil_spcg(double vl, double vf, params* q) {
	p_gipps* p = (p_gipps*)PICK(q, pars);
	return 3 * vf * p->tau / 2 + std::pow(vl, 2) / (2 * p->bg) - std::pow(vf, 2) / (2 * p->bn) + p->sn;
}

double gipps::wave_speed(Point* /* leader */, Point* /* follower */, params* /* q */) {
	return 0.0;
}

double gipps::free_flow_speed(params *q) {
	p_gipps* p = (p_gipps*)PICK(q, pars);
	return p->vn;
}

Point* gipps::new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* q) {
	p_gipps* p = (p_gipps*)PICK(q, pars);
	Point* cl = nullptr;
	if (leader != nullptr) cl = leader->operator[]( -(int)(p->tau / Clock::dt));

	//Euler by default
	double a = accel(cl, follower->operator[]( -(int)(p->tau / Clock::dt)), p);
	Point* pf = follower->get_current_point();
	double v = pf->V() + a * Clock::dt;
	double x = pf->X() + pf->V() * Clock::dt;
	double t = pf->T() + Clock::dt;
	return new Point(t, x, v, a, pf->LANE());
}
