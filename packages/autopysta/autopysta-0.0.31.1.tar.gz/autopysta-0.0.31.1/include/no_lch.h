/**
 * @file no_lch.h
 * @author Rafael Delpiano.
 * @date 11 dec 2019
 * @brief File for the definition of the `no_lch` class.
 *
 * @details This file contains the class definition for a lane-changing model
 * that prohibits any lane changes. This is a placeholder model for scenarios
 * where lane-changing behavior is not desired or applicable.
 */

#ifndef _NOLCH
#define _NOLCH

#include "models/model.h"

/**
 * @class no_lch
 * @brief A lane-changing model that forbids any lane changes.
 *
 * This class represents a model where no lane-changing maneuvers are allowed.
 * It acts as a fallback or placeholder model when lane-changing is not
 * considered in a traffic simulation.
 */
class no_lch : public LCM {
    /**
     * @brief Determine if a lane change is possible.
     *
     * This function always returns `false`, since lane changes are disallowed
     * in this model.
     *
     * @param leader The current leader's position and speed (optional).
     * @param follower The subject vehicle's position and speed.
     * @param new_leader The position and speed of the new leader after lane change (optional).
     * @param new_follower The position and speed of the new follower after lane change (optional).
     * @param cfpars Car-following model parameters.
     * @param lcmpars Lane-changing model parameters.
     * @return Always returns `false`.
     */
    bool is_lch_possible(Point *leader, Point *follower, Point *new_leader, Point *new_follower, Model *cfpars, params *lcmpars) override;

public:
    /**
     * @brief Default constructor for the `no_lch` model.
     *
     * Initializes the lane-changing model with no parameters and prohibits all
     * lane changes.
     */
    no_lch();

    /**
     * @brief Determine if the vehicle should change lanes to the left.
     *
     * Always returns `false` since lane changes are disallowed.
     *
     * @param leader The current leader's position and speed (optional).
     * @param follower The subject vehicle's position and speed.
     * @param new_leader The position and speed of the new leader after lane change (optional).
     * @param new_follower The position and speed of the new follower after lane change (optional).
     * @param cfm A car-following model.
     * @param lcmpars Lane-changing model parameters.
     * @return Always returns `false`.
     */
    bool lch_left(Point *leader, Point *follower, Point *new_leader, Point *new_follower, Model *cfm, params *lcmpars) override;

    /**
     * @brief Determine if the vehicle should change lanes to the right.
     *
     * Always returns `false` since lane changes are disallowed.
     *
     * @param leader The current leader's position and speed (optional).
     * @param follower The subject vehicle's position and speed.
     * @param new_leader The position and speed of the new leader after lane change (optional).
     * @param new_follower The position and speed of the new follower after lane change (optional).
     * @param cfm A car-following model.
     * @param lcmpars Lane-changing model parameters.
     * @return Always returns `false`.
     */
    bool lch_right(Point *leader, Point *follower, Point *new_leader, Point *new_follower, Model *cfm, params *lcmpars) override;

    ~no_lch() override = default;
};

#endif
