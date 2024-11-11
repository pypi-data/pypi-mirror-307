#include "models/newell_constrained_timestep.h"

newell_constrained_timestep::newell_constrained_timestep() : newell() {}

newell_constrained_timestep::newell_constrained_timestep(p_newell* p) : newell(p) {}

void newell_constrained_timestep::validate_parameters(params* /* p */) {
	double epsilon = 0.00001f;
	if (abs(tau - Clock::dt) > epsilon) {
		throw Exception(901, "Wrong parameters. 1/wkj (tau) must be equal to dt.");
	}
}

Point* newell_constrained_timestep::new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p)
{
	//Newell's model is not driven by a second-order ecuation with standard Euler approximation
	p_newell* q = (p_newell*)PICK(p, pars);
	int tau_steps = -(int)(tau / Clock::dt);
	Point* subject = follower->get_current_point();
	double nx = subject->X() + q->u*Clock::dt;
	double nv = q->u;
	double nt = subject->T() + Clock::dt;

	if (leader != nullptr) {
		Point* delayed_leader = (*leader)[tau_steps];
		double xc = delayed_leader->X() - sj;
		if (xc < subject->X()) xc = subject->X();
		if (xc < nx) {
			nv = delayed_leader->V();
			nx = xc;
		}
	}

	return new Point(
					nt,
					nx,
					nv,
					(nv - subject->V()) / Clock::dt,
					subject->LANE());
}
