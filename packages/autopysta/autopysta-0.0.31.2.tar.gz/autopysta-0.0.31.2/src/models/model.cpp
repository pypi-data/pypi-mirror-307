#include "models/model.h"

void Model::validate_parameters(params* /* p */) {}

Point* Model::new_point(Point* leader, Point* follower, params* p)
{
	//euler by default
	double a = accel(leader, follower, p);
	double v = follower->V() + a * Clock::dt;
	double x = follower->X() + follower->V() * Clock::dt;
	double t = follower->T() + Clock::dt;
	return new Point(t, x, v, a, follower->LANE());
}

Point* Model::new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p) {
	Point* cl = nullptr;
	if (leader != nullptr){
		cl = leader->get_current_point();
	}
	return new_point(cl, follower->get_current_point(), p);
}
