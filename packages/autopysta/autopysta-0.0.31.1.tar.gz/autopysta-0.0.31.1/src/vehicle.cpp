#include "vehicle.h"

#pragma region Vehicle Constructors
Vehicle::Vehicle(std::vector<double> hist_X, int lane)// Vehicle with a trajectory defined by every X, one lane only
{
	std::vector<int> lanes(hist_X.size(), lane); // Create a std::vector filled with the same lane with size equal to hist_X
	set_empty_points_queue(hist_X, lanes);
	needs_initialization = true;
	this->model = nullptr;

}

Vehicle::Vehicle(std::vector<double> hist_X, std::vector<int> lanes)// Vehicle with a trajectory defined by every X, multiple lanes allowed
{
	if (hist_X.size() != lanes.size()) {
		throw Exception(901, "Wrong parameters. hist_X must be the same size as lanes");
	}
	set_empty_points_queue(hist_X, lanes);
	needs_initialization = true;
	this->model = nullptr;
}

Vehicle::Vehicle(std::vector<Point*> hist_point) // Vehicle with a Trajectory defined by a std::vector of points (the points include their lane)
{
	if (hist_point.size() <= 1) {
		throw Exception(904, "Trajectory too short.");
	}

	for (std::vector<Point*>::iterator it = hist_point.begin(); it != hist_point.end(); ++it) {
		Point* fixed_p = *it;
		defined_t.push(fixed_p);
	}

	trajectory = new Trajectory(defined_t.front());
	defined_t.pop();
	this->model = nullptr;
}

Vehicle::Vehicle(Model* model, double position, double speed, int lane) {
	// If Clock::dt is null it means this constructor is being 
	// called before running the simulation, therefore 
	// its T doesnt matter as its going to be resetted on the
	// simulation::insert_vehicle method
	if (Clock::dt != 0.0) {
		trajectory = new Trajectory(new Point(Clock::time + Clock::dt, position, speed, 0, lane));
	} else {
		trajectory = new Trajectory(new Point(0.0, position, speed, 0, lane));
	}
	this->model = model;
}

Vehicle::Vehicle(Model* model, Point* point) {
	trajectory = new Trajectory(point);
	this->model = model;
}
#pragma endregion

#pragma region Vehicle Methods

void Vehicle::set_empty_points_queue(std::vector<double> hist_X, std::vector<int> lanes) {
	if (hist_X.size() <= 1) {
		throw Exception(904, "Trajectory too short.");
	}

	for (std::size_t step = 0; step < hist_X.size(); step++) {
		placeholder_points.push_back(new Point(0.0, hist_X.at(step), 0.0, 0.0, lanes.at(step)));
	}
}

void Vehicle::initialize_vehicle(){
	for (std::size_t time_step = 0; time_step < placeholder_points.size(); time_step++) {
		int lane = placeholder_points.at(time_step)->LANE();
		double fixed_x, fixed_v, fixed_a;
		double x_1, v_1;
		double x_2;

		fixed_x = placeholder_points.at(time_step)->X();
		fixed_v = 0;
		fixed_a = 0;

		if (time_step + 1 <= placeholder_points.size() - 1) {
			x_1 = placeholder_points.at(time_step + 1)->X();
			fixed_v = (x_1 - fixed_x) / Clock::dt;
		}

		if (time_step + 2 <= placeholder_points.size() - 1) {
			x_2 = placeholder_points.at(time_step + 2)->X();
			v_1 = (x_2 - x_1) / Clock::dt;
			fixed_a = (v_1 - fixed_v) / Clock::dt;
		}

		defined_t.push(new Point(Clock::dt * time_step, fixed_x, fixed_v, fixed_a, lane));
	}

	// Deestory the std::vector
	std::vector<Point*>().swap(placeholder_points);

	trajectory = new Trajectory(defined_t.front());
	defined_t.pop();
}

params* Vehicle::p()
{
	return model->pars;
}

Point* Vehicle::current() const
{
	return trajectory->get_current_point();
}

void Vehicle::update(Point *pt)
{
	if (pt != nullptr) ((Trajectory*)trajectory)->push_back(pt);
	// updation_check = !updation_check;
}

void Vehicle::update(RoadObject *leader) {
	GeneralizedTrajectory* leader_traj = nullptr;
	Point* new_point = nullptr;
	if (leader != nullptr){
		leader_traj = leader->trajectory; // current();
	}

	if (model != nullptr){
		new_point = model->new_point(leader_traj, (Trajectory*)trajectory);
		if (new_point->V() < 0) {
			new_point->set_x(this->current()->X());
			new_point->set_velocity(0.0);
			new_point->set_accel(0.0 - this->current()->V());
		}
	}
	else if (defined_t.size() > 0) { 
		new_point = defined_t.front();
		check_dt(new_point);
		defined_t.pop();
	}
	else if (defined_t.size() == 0) { 
		throw Exception(908, "Vehicle with given trajectory run out of points for the simulation");
	}
	update(new_point);	
}

void Vehicle::check_dt(Point* new_point) {
	double epsilon = 0.0000001f;
	if (abs((new_point->T() - current()->T()) - Clock::dt)>epsilon) {
		throw Exception(903, "Vehicle deltaTimes don't match");
	}
}

Vehicle::~Vehicle()
{
	delete trajectory;
}
#pragma endregion

#pragma region Fixed Object Constructor
FixedObject::FixedObject(Point *pos) { 
	this->pos = pos;
	trajectory = new StaticTrajectory(pos);
	model = nullptr;
}
#pragma endregion
#pragma region Fixed Object Methods

Point* FixedObject::current() const {
	return pos;
}

void FixedObject::update(RoadObject *) {}

#pragma endregion
