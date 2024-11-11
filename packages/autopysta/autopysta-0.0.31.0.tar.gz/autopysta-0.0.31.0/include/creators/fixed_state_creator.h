/**
 * @file fixed_state_creator.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Defines the `FixedStateCreator` class for generating vehicles with fixed spacing and speed.
 *
 * @details The `FixedStateCreator` class generates vehicles with a specified initial spacing and speed.
 *          Vehicles are placed at the beginning of a lane or behind a leader if one exists.
 */

#ifndef FIXED_STATE_CREATOR_H
#define FIXED_STATE_CREATOR_H

#include "creators/creator.h"


/**
 * @brief Vehicle creator that injects vehicles with a fixed state (spacing and speed).
 *
 * The `FixedStateCreator` class generates vehicles based on a specified spacing and initial speed.
 * Vehicles are placed at the start of the lane, or just behind a leader, if a leader vehicle is present.
 * This class is typically used for scenarios where vehicles need to maintain a fixed headway and speed.
 */
class FixedStateCreator : public Creator {
private:
    double target_spacing;   //!< Desired spacing between consecutive vehicles.
    double initial_speed;    //!< Initial speed for each newly created vehicle.
    
    /**
     * @brief Computes the ideal conditions for creating a new vehicle.
     *
     * This function calculates the optimal starting point and state for a new vehicle based on the
     * current state of the leader vehicle.
     *
     * @param leader A pointer to the current leader vehicle's point.
     * @return A point representing the ideal state for the new vehicle.
     */
    Point* calculate_ideal_conditions(Point* leader) override;

public:
    /**
     * @brief Validates the parameters of the fixed-state vehicle creator.
     *
     * Ensures that the model parameters are valid and the spacing is appropriate for the simulation.
     * If the parameters are invalid, an error will be thrown.
     */
    void validate_creator() override;

    /**
     * @brief Constructs a fixed-state vehicle creator.
     *
     * This constructor creates a vehicle creator with specified model, spacing, and initial speed. It also
     * allows limiting the maximum number of vehicles to be created.
     *
     * @param model A car-following model governing the lane's capacity.
     * @param spacing Target spacing between vehicles.
     * @param speed Initial speed for the created vehicles.
     * @param max_vehicles Maximum number of vehicles to create.
     */
    FixedStateCreator(Model* model, double spacing, double speed, int max_vehicles);

    /**
     * @brief Constructs a fixed-state vehicle creator.
     *
     * This constructor creates a vehicle creator with specified model, spacing, and initial speed.
     *
     * @param model A car-following model governing the lane's capacity.
     * @param spacing Target spacing between vehicles.
     * @param speed Initial speed for the created vehicles.
     */
    FixedStateCreator(Model* model, double spacing, double speed);

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
