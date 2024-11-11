/**
 * @file trajectory.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Contains definitions for the `GeneralizedTrajectory`, `StaticTrajectory`, and `Trajectory` classes.
 *
 * @details This file defines the base `generalized_trajectory` class, along with two derived classes:
 *          `trajectory` and `static_trajectory`. These classes manage the positions and movements of objects 
 *          on the road (either dynamic vehicles or static objects).
 */

#ifndef TRAJECTORY_H
#define TRAJECTORY_H

#include <vector>
#include "point.h"
#include "clock.h"
#include "exception.h"

/**
 * @brief Base class for different types of trajectories.
 *
 * This class provides an interface for retrieving points in a trajectory. Both `trajectory` and 
 * `static_trajectory` classes inherit from this class.
 */
class GeneralizedTrajectory {
public:
	/**
	 * @brief Get the current point of the trajectory.
	 * 
	 * @return Pointer to the current point.
	 */
	virtual Point* get_current_point() = 0;

	/**
	 * @brief Get a point by integer index.
	 *
	 * @param index Integer index of the point.
	 * @return Pointer to the point at the specified index.
	 */
	virtual Point* operator[](int index) const = 0;

	/**
	 * @brief Get a point by interpolating a floating-point index.
	 *
	 * @param index Floating-point index of the point.
	 * @return Pointer to the interpolated point.
	 */
	virtual Point* operator[](double index) const = 0;

	/**
	 * @brief Default constructor of GeneralizedTrajectory.
	 */
	virtual ~GeneralizedTrajectory() = default;
};

/**
 * @brief Represents a dynamic trajectory of a moving object.
 *
 * This class stores a series of `point` objects that define the trajectory of a moving vehicle.
 * It allows retrieving points using integer or floating-point indices, and handles extrapolation
 * for negative indices.
 */
class Trajectory: public std::vector<Point*>, public GeneralizedTrajectory {
	bool is_clock_updated; //!< Tracks whether the clock has been updated since the last point was added.

	/**
	 * @brief Extrapolates a point in the trajectory based on a negative index.
	 *
	 * @param index Negative index used to extrapolate a point.
	 * @return Extrapolated point.
	 * @throw Exception If the index is non-negative.
	 */
	Point* extrapolate(double index) const;

public:
	/**
	 * @brief Constructs a trajectory with an initial starting point.
	 *
	 * @param starting_point Initial point of the trajectory.
	 */
	Trajectory(Point* starting_point);

	/**
	 * @brief Adds a point to the trajectory.
	 *
	 * @param point Pointer to the point to add.
	 */
	void push_back(Point* point);

	/**
	 * @brief Adds a point to the trajectory.
	 *
	 * @param point Pointer to the point to add.
	 */
	void add_point(Point* point);


	/**
	 * @brief Adds a point and returns it.
	 *
	 * @param new_point Pointer to the new point to add.
	 * @return The added point.
	 */
	Point* add_and_return(Point* new_point);

	/**
	 * @brief Retrieves a point at the specified index.
	 *
	 * @param index Index of the point to retrieve.
	 * @return Pointer to the point at the specified index.
	 */
	Point* get_point_at(int index);

	/**
	 * @brief Returns the length of the trajectory.
	 *
	 * @return Number of points in the trajectory.
	 */
	int get_trajectory_length();

	/**
	 * @brief Gets the current position of the vehicle in the trajectory.
	 *
	 * @return The current point.
	 */
	Point* get_current_point() override;

	/**
	 * @brief Retrieves a point by integer index.
	 *
	 * @param index Index of the point to retrieve.
	 * @return Pointer to the point at the given index.
	 */
	Point* operator[](int index) const override;

	/**
	 * @brief Retrieves a point by floating-point index using interpolation.
	 *
	 * @param index Floating-point index for interpolating the point.
	 * @return Interpolated point.
	 */
	Point* operator[](double index) const override;
};

/**
 * @brief Represents a static trajectory for a fixed object on the road.
 *
 * This class handles the trajectory of static objects (such as a fixed vehicle or roadblock).
 */
class StaticTrajectory : public GeneralizedTrajectory {
	Point* position; //!< The position of the static object.

public:
	/**
	 * @brief Constructs a static trajectory with a fixed position.
	 *
	 * @param fixed_position The position of the static object.
	 */
	StaticTrajectory(Point* fixed_position);

	/**
	 * @brief Returns the current position of the static object.
	 *
	 * @return The current position as a point.
	 */
	Point* get_current_point() override;

	/**
	 * @brief Retrieves the point by integer index (always returns the static position).
	 *
	 * @param index Unused index parameter.
	 * @return The current position.
	 */
	Point* operator[](int index) const override;

	/**
	 * @brief Retrieves the point by floating-point index (always returns the static position).
	 *
	 * @param index Unused index parameter.
	 * @return The current position.
	 */
	Point* operator[](double index) const override;
};

#endif
