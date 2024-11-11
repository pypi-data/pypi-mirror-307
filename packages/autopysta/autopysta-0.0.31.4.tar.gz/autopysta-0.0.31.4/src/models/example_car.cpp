#include "models/example_car.h"


example_car::example_car(std::vector<Point*> t) {
	for (auto p = t.begin(); p != t.end(); p++) {
		defined_trajectory.push(*p);
	}
}

double example_car::accel(Point* /* leader */, Point* /* follower */, params* /* p */) {
    return 0;
}

double example_car::equil_spcg(double /* vl */, double /* vf */, params* /* p */) {
    return 0;
}

double example_car::wave_speed(Point* /* leader */, Point* /* follower */, params* /* p */) {
    return 0;
}

double example_car::free_flow_speed(params* /* q */) {
    return 0;
}

Point* example_car::new_point(GeneralizedTrajectory* /* leader */, Trajectory* /* follower */, params* /* p */) {
    Point* np = defined_trajectory.front();
    defined_trajectory.pop();
    return np;
}
