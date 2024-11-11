#include "trajectory.h"


#pragma region Trajectory

Trajectory::Trajectory(Point* startingPoint): vector<Point*>()
{
	vector::push_back(startingPoint);
	is_clock_updated = Clock::is_updated;
}

/*
trajectory::trajectory(Point* from[], int len, int skip=0)
{
	this->assign(from + skip, from + len);
	update_check = Clock::is_updated;
};
*/

void Trajectory::push_back(Point* point)
{
	vector::push_back(point);
	is_clock_updated = !is_clock_updated;
}

void Trajectory::add_point(Point* point)
{
	vector::push_back(point);
	is_clock_updated = !is_clock_updated;
}


Point* Trajectory::add_and_return(Point* newPoint)
{
	this->add_point(newPoint);
	return newPoint;
}

Point* Trajectory::get_point_at(int index)
{
	return (*this)[index];
}

int Trajectory::get_trajectory_length()
{	int size=(*this).size();
	return size;
}

Point* Trajectory::get_current_point()
{
	if (is_clock_updated == Clock::is_updated) {
		return back();
	}
	else {
		return *(end() - 2);
	}
}

Point* Trajectory::extrapolate(double index) const
{
	if (index >= 0) throw Exception(909, "Wrong index. Can't extrapolate");

	Point* first = operator[](0);
	return new Point(
		first->T() + index * Clock::dt,
		first->X() + index * Clock::dt * first->V(),
		first->V(),
		0,
		first->LANE()
	);
}

Point* Trajectory::operator[](double index) const
{
	int size = this->size();
	if (index > size - 1) throw Exception(909, "Wrong index. Can't return a Point of the future");

	double epsilon = 0.00001f;
	if (abs(index - (int)(index)) < epsilon) {
		return (*this)[(int)index];
	}

	if (index >= 0) {
		int predecessorIdx = (int)index;
		int successorIdx = (int)index + 1;
		Point* pred = ((vector<Point*>)(*this))[predecessorIdx];
		Point* succ = ((vector<Point*>)(*this))[successorIdx];

		float t = pred->T() + ((index - (int)index) * Clock::dt);
		float x = pred->X() + (succ->V() * (t - pred->T()));
		float v = (x - pred->X()) / (t - pred->T());
		float a = (v - pred->V()) / (t - pred->T());

		return new Point(t, x, v, a, pred->LANE());
	}

	// For negative indices
	float correctedIndex = size + index - (is_clock_updated == Clock::is_updated ? 0 : 1);
	if (correctedIndex < 0) {
		return this->extrapolate(correctedIndex);
	}
	return this->operator[](correctedIndex);
}


Point* Trajectory::operator[](int index) const
{
	int size = this->size();
	if (index >= size) throw Exception(909, "Wrong index. Can't return a Point of the future");

	if (index >= 0) return ((vector<Point*>)(*this))[index];

	// For negative indices, returns extrapolated point if out of range
	int correctedIndex = size + index - (is_clock_updated == Clock::is_updated ? 0 : 1);
	if (correctedIndex < 0) {
		return this->extrapolate(correctedIndex);
	}
	return this->operator[](correctedIndex);
}

#pragma endregion

#pragma region StaticTrajectory

StaticTrajectory::StaticTrajectory(Point* fixedPosition)
{
	this->position = fixedPosition;
}

Point* StaticTrajectory::get_current_point()
{
	return position;
}

Point* StaticTrajectory::operator[](int) const
{
	return position;
}

Point* StaticTrajectory::operator[](double) const
{
	return position;
}

#pragma endregion
