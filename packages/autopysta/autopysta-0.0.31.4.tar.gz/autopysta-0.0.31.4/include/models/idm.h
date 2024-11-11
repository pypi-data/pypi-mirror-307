/**
 * @file idm.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Definition of the IDM (Intelligent Driver Model) class.
 * 
 * @details This file defines the IDM class, which implements the Intelligent Driver Model 
 * (IDM) for traffic flow simulation. The IDM is a microscopic car-following model that 
 * captures various traffic phenomena such as free-flow traffic, congestion, and stop-and-go waves. 
 * The model parameters are calibrated based on empirical observations and microscopic simulations.
 * 
 * @see "Congested traffic states in empirical observations and microscopic simulations," 
 * Martin Treiber, Ansgar Hennecke, and Dirk Helbing, Phys. Rev. E 62, 1805 (2000).
 */

#ifndef _IDM_H
#define _IDM_H

#include <cmath>
#include "params/p_idm.h"
#include "model.h"
#include "point.h"

/**
 * @class idm
 * @brief The Intelligent Driver Model (IDM) for car-following behavior.
 * 
 * This class implements the IDM, a widely used microscopic traffic model for simulating 
 * car-following behavior. The model computes the acceleration of vehicles based on the 
 * distance to the leading vehicle, the relative velocity, and various model parameters.
 * 
 * The IDM captures the transition between free-flow, congested traffic, and stop-and-go waves 
 * based on a nonlinear formulation of acceleration and braking.
 * 
 * @note Reference: M. Treiber, A. Hennecke, and D. Helbing, "Congested traffic states in empirical 
 * observations and microscopic simulations," Phys. Rev. E, 62, 1805 (2000).
 */
class idm : public Model {
private:
    /**
     * @brief Computes the acceleration of a follower vehicle.
     * 
     * This method computes the acceleration of the follower vehicle based on the position and 
     * velocity of the leader and follower vehicles, using the IDM parameters. The acceleration 
     * depends on the distance to the leader, the relative speed, and desired speed, and it 
     * guarantees collision avoidance by dynamically adjusting the acceleration.
     * 
     * @param leader A point representing the leader's position and velocity. If null, free-flow behavior is assumed.
     * @param follower A point representing the follower's position and velocity.
     * @param q Pointer to the IDM model parameters.
     * @return The acceleration of the follower vehicle.
     */
    double accel(Point* leader, Point* follower, params* q) override;

    /**
     * @brief Computes the desired minimum gap between two vehicles.
     * 
     * This method calculates the desired minimum gap between the leader and the follower vehicles 
     * based on their velocities. The gap increases with higher velocities and can be influenced 
     * by parameters such as the desired time headway and vehicle length.
     * 
     * @param vl Velocity of the leader vehicle.
     * @param vf Velocity of the follower vehicle.
     * @param q Pointer to the IDM parameters. If null, default parameters are used.
     * @return The desired minimum gap.
     */
    double desired_minimum_gap(double vl, double vf, params* q = nullptr);


    virtual ~idm() = default;

public:
    /**
     * @brief Default constructor for the IDM model.
     * 
     * Initializes the IDM model with default parameters.
     */
    idm();

    /**
     * @brief Constructor for the IDM model with custom parameters.
     * 
     * Initializes the IDM model with custom parameters specified in the `p_idm` parameter object.
     * 
     * @param pars Pointer to the IDM-specific parameters.
     */
    idm(p_idm* pars);

    /**
     * @brief Computes the equilibrium spacing between the leader and follower.
     * 
     * Calculates the equilibrium spacing based on the velocities of the leader and follower vehicles. 
     * The equilibrium spacing increases with the follower's speed and is influenced by parameters 
     * like the safe time headway and jam distance.
     * 
     * @param vl Velocity of the leader.
     * @param vf Velocity of the follower.
     * @param q Pointer to the IDM parameters. If null, default parameters are used.
     * @return The equilibrium spacing.
     */
    double equil_spcg(double vl, double vf, params* q = nullptr) override;

    /**
     * @brief Computes the wave speed in a traffic disturbance.
     * 
     * Calculates the wave speed of a traffic disturbance, typically returning 0 unless overridden.
     * 
     * @param leader A point representing the leader's position and velocity.
     * @param follower A point representing the follower's position and velocity.
     * @param p Pointer to the IDM parameters.
     * @return The wave speed.
     */
    double wave_speed(Point* leader, Point* follower, params* p) override;

    /**
     * @brief Returns the free-flow speed of the IDM model.
     * 
     * The free-flow speed is the speed that vehicles would travel at in the absence of traffic.
     * 
     * @param p Pointer to the IDM parameters. If null, default parameters are used.
     * @return The free-flow speed.
     */
    double free_flow_speed(params* p = nullptr) override;
};

#endif // _IDM_H

