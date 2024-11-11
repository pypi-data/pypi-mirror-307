/**
 * @file creator.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Defines the `creator` class for generating vehicles in traffic simulations.
 *
 * @details The `creator` class provides an interface to generate vehicles in a traffic simulation,
 *          using specific models and conditions. The class is responsible for initializing vehicles
 *          at the start of the simulation and adding vehicles dynamically based on traffic conditions.
 */

#ifndef CREATOR_H
#define CREATOR_H

#include "params/params.h"
#include "models/model.h"
#include <iostream>
#include <vector>
#include <climits>
#include "point.h"
#include "trajectory.h"
#include "vehicle.h"

/**
 * @brief Base class for generating vehicles in a traffic simulation.
 *
 * The `creator` class defines the logic for creating new vehicles either at the start of the simulation
 * or during runtime. It handles the vehicle creation process based on specified models, parameters, and
 * traffic conditions (such as gaps between vehicles). Derived classes should implement specific creation logic.
 */
class Creator {
protected:
    int max_vehicles = INT_MAX;   //!< Maximum number of vehicles that can be created.
    int vehicle_count = 0;        //!< Counter for the number of vehicles created so far.
    Model* traffic_model = nullptr; //!< Traffic model used to determine vehicle behavior.

    /**
     * @brief Defines the ideal conditions for creating a new vehicle.
     *
     * This method computes the optimal starting position and behavior of a new vehicle based on
     * the position and speed of a leader vehicle. The derived classes must implement the specific
     * logic for defining these conditions.
     *
     * @param leader The point representing the current state (position and speed) of the leader vehicle.
     * @return A point representing the ideal conditions for the new vehicle.
     */
    virtual Point* calculate_ideal_conditions(Point* leader) = 0;

    virtual ~Creator() = default;

public:
    /**
     * @brief Validates the configuration of the creator.
     *
     * This method validates the configurations of the creator, such as ensuring that the maximum
     * number of vehicles and the model are properly set. This ensures that vehicle creation follows
     * the expected limits and behavior.
     */
    virtual void validate_creator();

    /**
     * @brief Creates a new vehicle based on the current leader's position.
     *
     * This method checks whether it is possible to create a new vehicle based on the leader's state.
     * If so, it generates a new vehicle at an appropriate position relative to the leader. If
     * `immediate_follower` is true, the new vehicle will be placed just behind the leader; otherwise,
     * it will start at the beginning of the lane.
     *
     * @param leader The point representing the leader's current state (position, speed).
     * @param immediate_follower Whether the new vehicle should follow immediately behind the leader.
     * @return A pointer to the created vehicle, or `nullptr` if no vehicle was created.
     */
    virtual Vehicle* create(Point* leader, bool immediate_follower = false);

    /**
     * @brief Creates a new vehicle in an empty lane.
     *
     * This method creates a new vehicle in a lane that has no leading vehicle. It is meant to be
     * used for initializing lanes with vehicles at the beginning of the simulation or adding vehicles
     * dynamically when no leader is present.
     *
     * @param lane The lane number in which to create the vehicle.
     * @return A pointer to the created vehicle, or `nullptr` if no vehicle was created.
     */
    virtual Vehicle* create_no_leader(int lane) = 0;

    /**
     * @brief Initializes vehicles in the first simulation timestep.
     *
     * This method is used to create and position vehicles during the first timestep of the simulation.
     * It generates vehicles behind a manually-created leading vehicle and populates the lane with vehicles
     * based on the traffic model.
     *
     * @param leader The manually-created leader vehicle.
     * @return A vector of pointers to the created vehicles.
     */
    std::vector<Vehicle*> initialize_state(Point* leader);
};

#endif // CREATOR_H
