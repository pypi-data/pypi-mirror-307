/**
 * @file model.h
 * @author Rafael Delpiano.
 * @date 11 dec 2019
 * @brief File for the model and lcm classes definitions (short description).
 *
 * @details A larger description about this file.
 * This is still part of the longer description.
 *
 * Another line.
 */

#ifndef MODEL_H
#define MODEL_H

#define PICK(x,y) (((x)==nullptr)?(y):(x))

#include "params/params.h"
#include "point.h"
#include "trajectory.h"
#include "clock.h"
#include "exception.h"

/**
 * @brief Abstract car-following model class.
 *
 * This class serves as the base for various car-following models, where vehicles adjust their
 * speed based on the behavior of a leading vehicle and certain model-specific parameters.
 */
class Model {
protected:
    /**
     * @brief Compute a vehicle's acceleration based on its leader.
     *
     * This method computes the acceleration of the subject vehicle (follower) based on the position
     * and speed of the leading vehicle (leader). If no leader is present, the behavior will depend 
     * on the model's specific implementation.
     *
     * @param leader A point representing the leader's position and speed. Can be null for no leader.
     * @param follower A point representing the subject vehicle's position and speed.
     * @param p Parameters for the model.
     * @return The computed acceleration.
     */
    virtual double accel(Point* leader, Point* follower, params* p) = 0;

public:
    params *pars; //!< Parameters for the car-following model.

    /**
     * @brief Validate the model parameters.
     *
     * Validates that the model's parameters meet certain constraints. This ensures that the model
     * works within its defined boundaries.
     *
     * @param p Parameters for the car-following model. If null, uses the model's internal parameters.
     */
    virtual void validate_parameters(params* p = nullptr);

    /**
     * @brief Compute the equilibrium spacing between vehicles.
     *
     * This method calculates the equilibrium spacing between the leader and follower vehicles
     * based on their velocities and model parameters.
     *
     * @param vl Leader's velocity.
     * @param vf Follower's velocity.
     * @param p Model parameters.
     * @return The equilibrium spacing.
     */
    virtual double equil_spcg(double vl, double vf, params* p = nullptr) = 0;

    /**
     * @brief Compute the wave speed of a traffic flow disturbance.
     *
     * This method computes the wave speed of traffic disturbances based on the leader's and follower's positions
     * and velocities.
     *
     * @param leader A point representing the leader's position and velocity.
     * @param follower A point representing the follower's position and velocity.
     * @param p Model parameters.
     * @return The computed wave speed (typically 0 unless overridden).
     */
    virtual double wave_speed(Point* leader, Point* follower, params *p) = 0;

    /**
     * @brief Get the free-flow speed of the model.
     *
     * This method returns the free-flow speed, which is the speed vehicles travel at when there are no
     * constraints (such as leading vehicles or road conditions).
     *
     * @param p Model parameters.
     * @return The free-flow speed.
     */
    virtual double free_flow_speed(params* p = nullptr) = 0;

    /**
     * @brief Compute the next point for a vehicle.
     *
     * Given the current positions of a leader and follower vehicle, this method calculates the next position
     * and speed of the follower.
     *
     * @param leader A point representing the leader's position and speed. Can be null for no leader.
     * @param follower A point representing the follower's position and speed.
     * @param p Model parameters.
     * @return A point representing the follower's next position and speed.
     */
    virtual Point* new_point(Point* leader, Point* follower, params* p = nullptr);

    /**
     * @brief Compute the next point for a vehicle using trajectories.
     *
     * This method computes the next position and speed of a follower vehicle based on the current trajectory
     * of both the leader and the follower.
     *
     * @param leader A generalized trajectory for the leader vehicle. Can be null for no leader.
     * @param follower A trajectory for the follower vehicle.
     * @param p Model parameters.
     * @return A point representing the follower's next position and speed.
     */
    virtual Point* new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p = nullptr);

    virtual ~Model() = default;

};

/**
 * @brief Abstract class for lane-changing models.
 *
 * This class handles the logic for determining whether a vehicle should change lanes based on
 * its current state, the state of nearby vehicles, and model-specific parameters.
 */
class LCM {
protected:
    Model* _cf;       //!< Car-following model used in conjunction with lane-changing decisions.
    params* _lcpars;  //!< Lane-changing model parameters.

    virtual ~LCM() = default;

    /**
     * @brief Check if a lane change is possible.
     *
     * This method determines whether a lane change is feasible, based on the position and speed of
     * the leader and follower in both the current lane and the target lane.
     *
     * @param leader Current leader in the lane.
     * @param follower Current follower in the lane.
     * @param new_leader New leader in the target lane.
     * @param new_follower New follower in the target lane.
     * @param cfpars Car-following model parameters.
     * @param lcmpars Lane-changing model parameters.
     * @return True if the lane change is feasible, false otherwise.
     */
    virtual bool is_lch_possible(Point* leader, Point* follower, Point* new_leader, Point* new_follower, Model* cfpars, params* lcmpars) = 0;

public:
    /**
     * @brief Determine if the vehicle should change lanes to the left.
     *
     * This method computes whether the subject vehicle should change lanes to the left, based on the
     * position and speed of nearby vehicles and the lane-changing model parameters.
     *
     * @param leader Current leader in the lane.
     * @param follower Current follower in the lane.
     * @param new_leader New leader in the target lane.
     * @param new_follower New follower in the target lane.
     * @param cfpars Car-following model parameters.
     * @param lcmpars Lane-changing model parameters.
     * @return True if the lane-changing maneuver is feasible, false otherwise.
     */
    virtual bool lch_left(Point* leader, Point* follower, Point* new_leader, Point* new_follower, Model* cfpars = nullptr, params* lcmpars = nullptr) = 0;

    /**
     * @brief Determine if the vehicle should change lanes to the right.
     *
     * This method computes whether the subject vehicle should change lanes to the right, based on the
     * position and speed of nearby vehicles and the lane-changing model parameters.
     *
     * @param leader Current leader in the lane.
     * @param follower Current follower in the lane.
     * @param new_leader New leader in the target lane.
     * @param new_follower New follower in the target lane.
     * @param cfpars Car-following model parameters.
     * @param lcmpars Lane-changing model parameters.
     * @return True if the lane-changing maneuver is feasible, false otherwise.
     */
    virtual bool lch_right(Point* leader, Point* follower, Point* new_leader, Point* new_follower, Model* cfpars = nullptr, params* lcmpars = nullptr) = 0;
};

#endif

