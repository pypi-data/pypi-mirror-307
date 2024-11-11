#include "point.h"

// Constructor with member initializer list
Point::Point(double initialTime, double initialPosition, double initialVelocity, double initialAcceleration, int initialLane)
    : time(initialTime), position(initialPosition), velocity(initialVelocity), acceleration(initialAcceleration), lane(initialLane) {}

// Copy constructor using a const reference
Point::Point(const Point& other)
    : time(other.T()), position(other.X()), velocity(other.V()), acceleration(other.A()), lane(other.LANE()) {}


// Converts the Point object to a string representation
std::string Point::to_string() const {
    std::stringstream ss;
    ss << "(time=" << time << ", position=" << position << ", velocity=" << velocity
       << ", acceleration=" << acceleration << ", lane=" << lane << ")";
    return ss.str();
}


// Getters
double Point::T() const {
    return time;
}

double Point::X() const {
    return position;
}

double Point::V() const {
    return velocity;
}

double Point::A() const {
    return acceleration;
}

int Point::LANE() const {
    return lane;
}



// Setters
void Point::set_accel(double newAcceleration) {
    acceleration = newAcceleration;
}

void Point::set_velocity(double newVelocity) {
    velocity = newVelocity;
}

void Point::set_x(double newPosition) {
    position = newPosition;
}

void Point::set_lane(int newLane) {
    lane = newLane;
}

// Resets the time to zero
void Point::reset_time() {
    time = 0;
}

