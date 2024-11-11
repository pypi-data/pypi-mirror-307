/**
 * @file linear.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Header file for the linear class definition.
 *
 * @details This file defines the linear car-following model, which computes vehicle accelerations based on the difference
 * in speed and spacing between the following and leader vehicles. The model considers factors such as desired speed,
 * response time, and spacing between vehicles.
 */

#ifndef LINEAR_H
#define LINEAR_H

#include<math.h>
#include "params/p_linear.h"
#include "model.h"
#include "point.h"

/**
 * @brief Linear car-following model.
 *
 * The linear car-following model is a simple model that calculates the acceleration of a vehicle based on a linear function
 * of the speed difference between the vehicle and the vehicle ahead (leader). It uses parameters such as free-flow speed,
 * reaction time, and spacing to simulate vehicle behavior in traffic flow.
 */
class linear : public Model {
private:
    //! Computes the acceleration of the follower vehicle.
    /*!
     * This function computes the acceleration based on the difference between the leader and follower's speeds and
     * positions. It uses the model's parameters to adjust for desired speed and spacing.
     *
     * \param leader The point representing the leader's position and speed. Can be null if no leader is present.
     * \param follower The point representing the follower's position and speed.
     * \param p Pointer to the linear model parameters.
     * \return The computed acceleration for the follower vehicle.
     */
    double accel(Point *leader, Point *follower, params *p) override;

public:
    //! Default constructor for the linear model.
    /*!
     * Initializes the linear model with default parameter values.
     */
    linear();
    
    //! Constructor with custom parameters.
    /*!
     * Initializes the linear model with custom parameters provided via the p_linear class.
     *
     * \param p A pointer to the p_linear parameter object containing the model's parameters.
     */
    linear(p_linear *p);

    //! Computes the equilibrium spacing between vehicles.
    /*!
     * This function calculates the equilibrium spacing between the leader and follower vehicles based on their velocities.
     * The equilibrium spacing depends on the free-flow speed, reaction time, and spacing parameters.
     *
     * \param vl The velocity of the leader vehicle.
     * \param vf The velocity of the follower vehicle.
     * \param p Pointer to the linear model parameters.
     * \return The equilibrium spacing between the vehicles.
     */
    double equil_spcg(double vl, double vf, params *p) override;
    
    //! Computes the wave speed in the model.
    /*!
     * The wave speed represents the speed at which traffic congestion propagates backward through a line of vehicles.
     * This function calculates the wave speed based on model parameters such as reaction time and spacing.
     *
     * \param leader The point representing the leader's position and speed.
     * \param follower The point representing the follower's position and speed.
     * \param p Pointer to the linear model parameters.
     * \return The computed wave speed.
     */
    double wave_speed(Point *leader, Point *follower, params *p) override;
    
    //! Returns the free-flow speed of the linear model.
    /*!
     * This function returns the free-flow speed, which is the speed at which vehicles travel in the absence of traffic congestion.
     * 
     * \param p Pointer to the linear model parameters.
     * \return The free-flow speed.
     */
    double free_flow_speed(params *p = nullptr) override;
};

#endif
