/**
 * @file newell.h
 * @author Rafael Delpiano
 * @date 11 Dec 2019
 * @brief Header file for Newell's car-following model class definition.
 * 
 * @details This file contains the class definition for the Newell car-following model. 
 * Newell's model is a simplified approach to simulating vehicle dynamics in traffic, 
 * based on translating the trajectory of the preceding vehicle by a fixed time gap (τ) 
 * and space gap (δ). The model is commonly used in traffic flow simulations.
 */

#ifndef _NEWELL
#define _NEWELL

#include <math.h>
#include "params/p_newell.h"
#include "models/model.h"
#include "point.h"
#include "clock.h"

/**
 * @brief Newell's car-following model (2002).
 * 
 * This class implements Newell's car-following model, which is a simplified model
 * that describes how vehicles follow one another in traffic. The model assumes that 
 * each vehicle follows the same trajectory as the vehicle in front but delayed by 
 * a time gap (τ) and space gap (δ). These parameters are derived from the wave 
 * speed (w) and jam density (kj), which are the core elements of the model.
 * 
 * @note Reference: Newell, G. F. (2002). "A Simplified Car-Following Theory: A Lower Order Model." 
 * Institute of Transportation Studies, University of California, Berkeley.
 */
class newell : public Model {
protected:
    float tau; //!< Time gap (τ) between the trajectories of the follower and the leader.
    float sj;  //!< Jam spacing (δ), the minimum distance between vehicles in a jam.

    /**
     * @brief Initializes the model parameters for Newell's model.
     * 
     * This function sets the time gap (τ) and jam spacing (δ) based on the wave speed
     * and jam density of the model.
     * 
     * @param p Pointer to the p_newell parameters containing wave speed and jam density values.
     */
    void initialize_parameters(p_newell* p);

    /**
     * @brief Computes the follower vehicle's acceleration based on the leader's position.
     * 
     * This method calculates the acceleration of the follower vehicle by translating 
     * the leader's position and velocity using Newell's piecewise linear trajectory rule.
     * 
     * @param leader A point representing the leader's position and velocity.
     * @param follower A point representing the follower's position and velocity.
     * @param p Parameters for Newell's model.
     * @return The calculated acceleration of the follower vehicle.
     */
    double accel(Point* leader, Point* follower, params* p) override;

    /**
     * @brief Computes the next point in the follower's trajectory.
     * 
     * This method determines the next position and velocity for the follower vehicle by 
     * translating the leader's trajectory by a time gap (τ) and space gap (δ).
     * 
     * @param leader A point representing the leader's position and velocity.
     * @param follower A point representing the follower's position and velocity.
     * @param p Parameters for Newell's model.
     * @return A point representing the follower's updated position and speed.
     */
    Point* new_point(Point* leader, Point* follower, params* p = nullptr) override;

    virtual ~newell() = default;

public:
    /**
     * @brief Default constructor for Newell's model.
     * 
     * This constructor initializes the model using default values for the wave speed (w),
     * jam density (kj), and free-flow speed.
     */
    newell();

    /**
     * @brief Constructor for Newell's model with custom parameters.
     * 
     * This constructor allows initializing the model with custom values for the wave speed,
     * jam density, and free-flow speed using the p_newell parameter class.
     * 
     * @param p Pointer to the p_newell class containing the parameters for Newell's model.
     */
    newell(p_newell* p);

    /**
     * @brief Computes the equilibrium spacing between the leader and follower vehicles.
     * 
     * This method calculates the equilibrium spacing between the leader and follower vehicles 
     * based on their velocities. The equilibrium spacing increases with higher speeds.
     * 
     * @param vl The velocity of the leader vehicle.
     * @param vf The velocity of the follower vehicle.
     * @param p Pointer to the parameters for Newell's model.
     * @return The computed equilibrium spacing between the vehicles.
     */
    double equil_spcg(double vl, double vf, params* p = nullptr) override;

    /**
     * @brief Returns the wave speed for Newell's model.
     * 
     * The wave speed represents the speed at which traffic disturbances propagate backward 
     * through a line of vehicles in congestion.
     * 
     * @param leader A point representing the leader's position and speed.
     * @param follower A point representing the follower's position and speed.
     * @param p Parameters for Newell's model.
     * @return The wave speed.
     */
    double wave_speed(Point* leader, Point* follower, params* p) override;

    /**
     * @brief Returns the free-flow speed for Newell's model.
     * 
     * The free-flow speed is the maximum speed at which vehicles travel when there is no congestion.
     * 
     * @param p Parameters for Newell's model.
     * @return The free-flow speed of the model.
     */
    double free_flow_speed(params* p = nullptr) override;

    /**
     * @brief Computes the next point in the follower's trajectory using generalized trajectories.
     * 
     * This method calculates the next point in the follower vehicle's trajectory by considering 
     * both the leader and follower's current trajectories. It applies Newell's piecewise linear 
     * trajectory rule to compute the follower's next position and velocity.
     * 
     * @param leader Generalized trajectory representing the leader vehicle's path.
     * @param follower Trajectory representing the follower vehicle's path.
     * @param p Parameters for Newell's model.
     * @return A point representing the follower's updated position and speed.
     */
    Point* new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p = nullptr) override;
};

#endif
