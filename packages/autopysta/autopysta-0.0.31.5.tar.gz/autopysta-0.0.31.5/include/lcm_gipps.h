/**
 * @file lcm_gipps.h
 * @author Rafael Delpiano.
 * @date 11 dec 2019
 * @brief File for the `lcm_gipps` and `p_lcm_gipps` classes definitions.
 *
 * @details This file contains the class definition for the Gipps (1986) lane-changing
 * model (`lcm_gipps`) and its parameter manager (`p_lcm_gipps`), which provides a
 * behavior-based model for vehicles changing lanes in traffic simulation.
 */

#ifndef _LCMGIPPS
#define _LCMGIPPS

#include "models/model.h"
#include "exception.h"

/**
 * @class p_lcm_gipps
 * @brief Parameter manager for the Gipps (1986) lane-changing model.
 *
 * This class handles the lane-changing parameters, including the fractions
 * of free-flow speed required to initiate overtaking (left lane change) and to
 * revert to the original lane (right lane change).
 */
class p_lcm_gipps : public params {
public:
    double _pvl; //!< Fraction of free-flow speed for overtaking (left lane change).
    double _pvh; //!< Fraction of free-flow speed for returning (right lane change).

    /**
     * @brief Default constructor for the Gipps lane-changing model parameters.
     *
     * Initializes parameters with default values: `_pvl = 0.9` and `_pvh = 0.95`.
     */
    p_lcm_gipps();

    /**
     * @brief Constructor with custom lane-changing parameters.
     *
     * Initializes parameters with the given values.
     *
     * @param pvlow Fraction of free-flow speed for overtaking (must be between 0 and 1).
     * @param pvhigh Fraction of free-flow speed for returning to the original lane (must be between `pvlow` and 1).
     * @throws Exception if the input values are not in the range 0 < `pvlow` < `pvhigh` < 1.
     */
    p_lcm_gipps(double pvlow, double pvhigh);
};

/**
 * @class lcm_gipps
 * @brief Lane-changing model based on the Gipps (1986) behavioral model.
 *
 * This class manages the functionality for vehicle lane-changing decisions,
 * according to the rules defined by Gipps's model. Vehicles decide when to
 * overtake or return to their original lane based on traffic conditions and
 * the parameters from the `p_lcm_gipps` class.
 */
class lcm_gipps : public LCM {
    /**
     * @brief Determine if a lane change is possible based on traffic conditions.
     *
     * This function checks whether a lane-changing maneuver is feasible based on
     * the positions and speeds of the leader and follower vehicles in both the
     * current and new lanes.
     *
     * @param leader Current leader in the lane.
     * @param follower Current vehicle's position and speed (follower).
     * @param new_leader The vehicle to become the subject's leader in the new lane.
     * @param new_follower The vehicle to become the subject's follower in the new lane.
     * @param cfpars Car-following model used to compute distances and speed.
     * @param lcmpars Lane-changing parameters.
     * @return True if the lane-changing maneuver is feasible, false otherwise.
     */
    bool is_lch_possible(Point *leader, Point *follower, Point *new_leader, Point *new_follower, Model *cfpars, params *lcmpars) override;

public:
    /**
     * @brief Default constructor for the Gipps lane-changing model.
     *
     * Initializes the model with default parameters.
     */
    lcm_gipps();

    /**
     * @brief Constructor for the Gipps lane-changing model with custom parameters.
     *
     * @param p Custom lane-changing parameters.
     */
    lcm_gipps(p_lcm_gipps *p);

    /**
     * @brief Determine if the vehicle should change lanes to the left.
     *
     * The decision to change lanes to the left is based on the vehicle's speed relative
     * to a fraction of the free-flow speed. If the speed is lower than a certain threshold,
     * the lane change will be considered.
     *
     * @param leader Current leader in the lane.
     * @param subject Current vehicle's position and speed (follower).
     * @param new_leader The vehicle to become the subject's leader in the new lane.
     * @param new_follower The vehicle to become the subject's follower in the new lane.
     * @param cfm A car-following model.
     * @param lcmpars Lane-changing model parameters.
     * @return True if the lane change to the left is feasible, false otherwise.
     */
    bool lch_left(Point *leader, Point *subject, Point *new_leader, Point *new_follower, Model *cfm, params *lcmpars) override;

    /**
     * @brief Determine if the vehicle should change lanes to the right.
     *
     * The decision to change lanes to the right is based on the vehicle's speed relative
     * to a fraction of the free-flow speed. If the speed is higher than a certain threshold,
     * the lane change will be considered.
     *
     * @param leader Current leader in the lane.
     * @param follower Current vehicle's position and speed (follower).
     * @param new_leader The vehicle to become the subject's leader in the new lane.
     * @param new_follower The vehicle to become the subject's follower in the new lane.
     * @param cfm A car-following model.
     * @param lcmpars Lane-changing model parameters.
     * @return True if the lane change to the right is feasible, false otherwise.
     */
    bool lch_right(Point *leader, Point *follower, Point *new_leader, Point *new_follower, Model *cfm, params *lcmpars) override;

    ~lcm_gipps() override = default;  // Virtual destructor

};

#endif
