/**
 * @file example_car.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Defines the `example_car` class, a simple car-following model.
 *
 * @details This file defines the `example_car` class, which provides a basic implementation of a car-following model.
 *          It uses a predefined trajectory to guide the vehicle's movement and updates the vehicle's state accordingly.
 */

#ifndef EXAMPLE_CAR_H
#define EXAMPLE_CAR_H

#include "models/model.h"
#include "point.h"
#include <queue>
#include <vector>

/**
 * @brief A simple car-following model with a predefined trajectory.
 *
 * The `example_car` class models vehicle behavior based on a predefined trajectory of points.
 * This class demonstrates basic car-following dynamics by returning points sequentially from its trajectory.
 */
class example_car : public Model {
private:
    std::queue<Point*> defined_trajectory; //!< Queue storing the predefined trajectory of the vehicle.

public:
    /**
     * @brief Constructor for the `example_car` model.
     *
     * Initializes the car with a predefined trajectory of points.
     *
     * @param t A vector of points representing the trajectory of the vehicle over time.
     */
    example_car(std::vector<Point*> t);

    /**
     * @brief Computes the acceleration of the follower vehicle.
     *
     * This function returns a default value of `0` for acceleration, as the model does not implement
     * dynamic acceleration behavior. It simply follows the predefined trajectory.
     *
     * @param leader A pointer to the leader vehicle's current point (can be `nullptr` if no leader).
     * @param follower A pointer to the follower vehicle's current point.
     * @param q Model-specific parameters.
     * @return Always returns `0`.
     */
    double accel(Point* leader, Point* follower, params* q) override;

    /**
     * @brief Computes the equilibrium spacing between vehicles.
     *
     * This function returns `0`, as the equilibrium spacing is not dynamically calculated in this model.
     *
     * @param vl The velocity of the leader vehicle.
     * @param vf The velocity of the follower vehicle.
     * @param q Model-specific parameters.
     * @return Always returns `0`.
     */
    double equil_spcg(double vl, double vf, params* q) override;

    /**
     * @brief Computes the wave speed of a traffic disturbance.
     *
     * This method returns `0`, as wave speed calculation is not implemented in this example model.
     *
     * @param leader A pointer to the leader vehicle's point.
     * @param follower A pointer to the follower vehicle's point.
     * @param q Model-specific parameters.
     * @return Always returns `0`.
     */
    double wave_speed(Point* leader, Point* follower, params* q) override;

    /**
     * @brief Returns the free-flow speed of the model.
     *
     * The method returns `0` for free-flow speed in this example model.
     *
     * @param q Model-specific parameters.
     * @return Always returns `0`.
     */
    double free_flow_speed(params* q) override;

    /**
     * @brief Retrieves the next point in the predefined trajectory.
     *
     * This method returns the next point in the predefined trajectory, removing it from the queue.
     * It does not compute new positions or velocities.
     *
     * @param leader A pointer to the leader vehicle's trajectory (can be `nullptr` if no leader).
     * @param follower A pointer to the follower vehicle's trajectory.
     * @param p Model-specific parameters (optional).
     * @return The next point in the trajectory.
     */
    Point* new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p = (params*)nullptr) override;
};

#endif
