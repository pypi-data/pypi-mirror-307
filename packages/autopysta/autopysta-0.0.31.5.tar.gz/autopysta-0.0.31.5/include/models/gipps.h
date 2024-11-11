/**
 * @file gipps.h
 * @author Rafael Delpiano
 * @date 11 Dec 2019
 * @brief Header file for the Gipps car-following model class.
 *
 * @details This file defines the Gipps car-following model, which simulates vehicle behavior 
 * in traffic streams based on a set of constraints related to acceleration, braking, and 
 * following distances. The model is useful for analyzing the impact of changes in traffic conditions 
 * on flow and vehicle response.
 */

#ifndef GIPPS_H
#define GIPPS_H

#include "params/p_gipps.h"
#include "models/model.h"
#include "point.h"
#include "exception.h"

#include <cmath>

/**
 * @brief Gipps car-following model (1981).
 *
 * This class implements the Gipps (1981) car-following model, which aims to simulate the 
 * behavior of vehicles in a traffic stream, particularly how a vehicle responds to the 
 * movement of the preceding vehicle. The model is based on realistic driver and vehicle 
 * behavior constraints such as maximum acceleration, braking, and desired speeds.
 * 
 * The model introduces two main constraints:
 * - A free acceleration component that limits acceleration as the vehicle approaches its desired speed.
 * - A braking component that ensures the vehicle can safely stop if the vehicle ahead brakes suddenly.
 * 
 * Reference: Gipps, P.G. (1981), "A Behavioural Car-Following Model for Computer Simulation", 
 * Transport Research Part B, Vol. 15, pp. 105-111.
 */
class gipps : public Model {
private:
    /** 
     * @brief Computes the vehicle's acceleration based on the leader's and follower's positions.
     * 
     * The acceleration is computed using two main constraints:
     * 1. A free acceleration term that limits the follower's acceleration as it approaches its desired speed.
     * 2. A braking term that ensures the follower can stop safely if the leader suddenly decelerates.
     *
     * @param leader A point representing the leader's position and speed. Leave null if no leader is present.
     * @param follower A point representing the follower's position and speed.
     * @param p Parameters for the Gipps model.
     * @return The computed acceleration value.
     */
    double accel(Point *leader, Point *follower, params *p) override;

    virtual ~gipps() = default;

public:
    /** 
     * @brief Default constructor for the Gipps model.
     * 
     * Initializes the model with default parameter values, including default values for 
     * maximum acceleration, braking, and reaction time.
     */
    gipps();

    /**
     * @brief Constructor with custom parameters for the Gipps model.
     * 
     * Initializes the model with a custom set of parameters, allowing the simulation to 
     * represent different vehicle and driver behaviors.
     * 
     * @param p A pointer to a p_gipps parameter class containing the custom parameters.
     */
    gipps(p_gipps *p);

    /**
     * @brief Validates the parameters of the Gipps model.
     * 
     * Ensures that the parameters for maximum acceleration, braking, and reaction time are 
     * non-zero and valid. If invalid, an exception is thrown.
     * 
     * @param p Parameters for the Gipps model. If null, the model uses its default parameters.
     */
    void validate_parameters(params* p = (params*)nullptr) override;

    /**
     * @brief Computes the equilibrium spacing between vehicles according to the Gipps model.
     * 
     * The equilibrium spacing is the safe distance that vehicles should maintain, accounting for 
     * the vehicle's speed and the driver's braking limits.
     * 
     * @param vl The velocity of the leader vehicle.
     * @param vf The velocity of the follower vehicle.
     * @param p Parameters for the Gipps model. If null, the model uses its default parameters.
     * @return The equilibrium spacing between the vehicles.
     */
    double equil_spcg(double vl, double vf, params *p = (params*)nullptr) override;

    /*!
     * This function is a placeholder for the wave speed calculation. In the Gipps model, 
     * the wave speed is not explicitly calculated.
     * 
     * @param leader A point representing the leader's position and speed.
     * @param follower A point representing the follower's position and speed.
     * @param p Parameters for the Gipps model.
     * @return Always returns zero (0.0).
     */
    double wave_speed(Point *leader, Point *follower, params *p) override;

    /**
     * @brief Computes the free-flow speed for the Gipps model.
     * The free-flow speed represents the maximum speed the vehicle can travel at, assuming 
     * there is no interaction with other vehicles ahead (i.e., no leader).
     * 
     * @param p Parameters for the Gipps model. If null, the model uses its default parameters.
     * @return The free-flow speed of the vehicle.
     */
    double free_flow_speed(params *p = (params*)nullptr) override;

    /**
     * @brief Computes the next point in the follower's trajectory based on the leader's movement.
     * This function computes the next position, speed, and acceleration of the follower vehicle 
     * based on the current position of both the leader and follower vehicles. The model applies 
     * both acceleration and braking constraints to ensure safe car-following behavior.
     * 
     * @param leader Generalized trajectory of the leader vehicle.
     * @param follower Trajectory of the follower vehicle.
     * @param p Parameters for the Gipps model. If null, the model uses its default parameters.
     * @return A new point representing the updated position, speed, and acceleration of the follower.
     */
    Point* new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p = (params*)nullptr) override;
};

#endif
