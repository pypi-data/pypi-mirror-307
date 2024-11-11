/**
 * @file fixed_demand_creator.h
 * @brief Defines the `fixed_demand_creator` class for generating vehicles at a fixed rate.
 *
 * @details The `fixed_demand_creator` class generates vehicles at a given flow rate. 
 *          Vehicles are placed at the beginning of a lane unless constraints prevent it.
 */

#ifndef FIXED_DEMAND_CREATOR_H
#define FIXED_DEMAND_CREATOR_H

#include <cmath>
#include "creators/creator.h"

/**
 * @brief Vehicle creator that injects vehicles at a fixed rate (flow).
 *
 * The `fixed_demand_creator` class generates vehicles based on a specified flow rate, placing
 * them at the beginning of a lane or behind a leader. Vehicles are injected at regular intervals
 * based on the desired headway.
 */
class FixedDemandCreator : public Creator {
private:
    double vehicle_headway;  //!< The headway (inverse of flow) between vehicles.
    double flow_rate;        //!< Flow rate or vehicle generation rate.

    /**
     * @brief Computes the ideal conditions for creating a new vehicle.
     *
     * This function calculates the optimal starting point and state for a new vehicle based on the
     * current state of the leader vehicle and the specified flow rate.
     *
     * @param leader A pointer to the current leader vehicle's point.
     * @return A point representing the ideal state for the new vehicle.
     */
    Point* calculate_ideal_conditions(Point* leader) override;

public:
    /**
     * @brief Constructs a fixed-demand vehicle creator.
     *
     * This constructor creates a vehicle creator that generates vehicles at a specified flow rate.
     *
     * @param model A car-following model governing the lane's capacity.
     * @param flow The target flow rate (vehicles per second).
     */
    FixedDemandCreator(Model* model, double flow);

    /**
     * @brief Constructs a limited fixed-demand vehicle creator.
     *
     * This constructor creates a vehicle creator that generates vehicles at a specified flow rate
     * with a limit on the maximum number of vehicles created.
     *
     * @param model A car-following model governing the lane's capacity.
     * @param flow The target flow rate (vehicles per second).
     * @param max_vehicles The maximum number of vehicles to create.
     */
    FixedDemandCreator(Model* model, double flow, int max_vehicles);

    /**
     * @brief Validates the flow rate parameters of the fixed-demand vehicle creator.
     *
     * This method checks that the specified flow rate is feasible given the time step (`dt`) of the
     * simulation. If the demand is not feasible, an exception will be thrown.
     */
    void validate_creator() override;

    /**
     * @brief Creates a new vehicle in a lane without a leader.
     *
     * This function generates a new vehicle in an empty lane if there is space, or returns `nullptr` if
     * no more vehicles can be created.
     *
     * @param lane The lane number where the vehicle is created.
     * @return A pointer to the created vehicle, or `nullptr` if no vehicle was created.
     */
    Vehicle* create_no_leader(int lane) override;
};

#endif
