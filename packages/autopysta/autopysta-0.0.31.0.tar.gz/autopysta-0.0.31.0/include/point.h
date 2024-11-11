/**
 * @file point.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief File for the point class definition.
 *
 * @details This file contains the definition of the point class, which 
 * represents a vehicle's position, velocity, acceleration, time, and lane in a traffic simulation.
 */

#ifndef _POINT
#define _POINT

#include<string>
#include<sstream>

/**
 * @brief Represents a point in time for a vehicle in a traffic simulation.
 * 
 * The point class stores and manages the time, position, velocity, 
 * acceleration, and lane of a vehicle during simulation.
 */
class Point{
private:
    double time;           //!< Time at this point.
    double position;       //!< Position on the road.
    double velocity;       //!< Velocity of the vehicle.
    double acceleration;   //!< Acceleration of the vehicle.
    int lane;              //!< Lane number.

public:
    /**
     * @brief Constructor for the Point class.
     * 
     * Initializes the Point object with specified time, position, velocity, 
     * acceleration, and lane.
     * 
     * @param time Initial time.
     * @param position Initial position.
     * @param velocity Initial velocity.
     * @param acceleration Initial acceleration.
     * @param lane Initial lane.
     */
    Point(double time, double position, double velocity, double acceleration, int lane);

    /**
     * @brief Copy constructor for the Point class.
     * 
     * Creates a new Point object by copying values from another Point object.
     * 
     * @param other Point object to duplicate.
     */
    Point(const Point& other);

    /**
     * @brief Converts the Point object to a string representation.
     * 
     * This function generates a string that represents the current state 
     * of the Point object.
     * 
     * @return A string representing the Point object.
     */
    std::string to_string() const;

    /**
     * @brief Sets the acceleration of the point.
     * 
     * @param newAcceleration New acceleration value.
     */
    void set_accel(double _a);

    /**
     * @brief Sets the velocity of the point.
     * 
     * @param newVelocity New velocity value.
     */
    void set_velocity(double _v);

    /**
     * @brief Sets the position of the point.
     * 
     * @param newPosition New position value.
     */
    void set_x(double _x);

    /**
     * @brief Sets the lane of the point.
     * 
     * @param newLane New lane value.
     */
    void set_lane(int _lane);

    /**
     * @brief Resets the time of the point to zero.
     * 
     * This function resets the time value of the point object to zero.
     */
    void reset_time();

    /**
     * @brief Gets the time value.
     * 
     * @return Current time value.
     */
    double T() const;

    /**
     * @brief Gets the position value.
     * 
     * @return Current position value.
     */
    double X() const;

    /**
     * @brief Gets the velocity value.
     * 
     * @return Current velocity value.
     */
    double V() const;

    /**
     * @brief Gets the acceleration value.
     * 
     * @return Current acceleration value.
     */
    double A() const;

    /**
     * @brief Gets the lane value.
     * 
     * @return Current lane value.
     */
    int LANE() const;
};

#endif
