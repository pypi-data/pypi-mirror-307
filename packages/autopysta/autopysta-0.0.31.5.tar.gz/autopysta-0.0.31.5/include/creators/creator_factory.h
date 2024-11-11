/**
 * @file creator_factory.h
 * @brief A factory class for creating different types of vehicle creators.
 *
 * @details The `CreatorFactory` class provides a convenient way to instantiate various `Creator` subclasses
 *          by specifying the type and relevant parameters. This pattern simplifies the instantiation logic
 *          and allows for flexible creator type selection.
 */

#ifndef CREATOR_FACTORY_H
#define CREATOR_FACTORY_H

#include "creators/creator.h"
#include "creators/fixed_demand_creator.h"
#include "creators/fixed_state_creator.h"
#include "creators/creator_martinez_jin_2020.h"

#include <string>
#include <stdexcept>

/**
 * @brief A factory class for creating different types of vehicle creators.
 *
 * The `CreatorFactory` class provides a convenient way to instantiate various `Creator` subclasses
 * by specifying the type and relevant parameters. This pattern simplifies the instantiation logic.
 */
class CreatorFactory {
public:
    /**
     * @brief Enum to specify the creator type.
     */
    enum CreatorType {
        FixedDemand,
        FixedState,
    };

    /**
     * @brief Creates a vehicle creator based on the specified type and parameters.
     *
     * This function returns a raw pointer to a `Creator` instance based on the `CreatorType`.
     * The `model` parameter is required for all types, while others are specific to the creator type.
     *
     * @param type The type of creator to instantiate.
     * @param model The traffic model used for vehicle creation.
     * @param flow Mean flow rate (vehicles per second), applicable for demand creators.
     * @param max_vehicles Max vehicles allowed, applicable for creators with a max limit.
     * @param spacing Desired spacing between vehicles, applicable for state creators.
     * @param speed Desired initial speed of vehicles, applicable for state creators.
     * @param variability Variability factor for stochastic creators.
     * @return A raw pointer to the instantiated creator.
     */
    static Creator* create_creator(
        CreatorType type,
        Model* model,
        double flow = 0,
        int max_vehicles = INT_MAX,
        double spacing = 0,
        double speed = 0,
        double variability = 0
    );

private:
    /**
     * @brief Validates input parameters based on creator type.
     *
     * Ensures that the parameters provided are appropriate for the specified creator type.
     * Throws exceptions for any invalid parameter combinations.
     *
     * @param type The type of creator to instantiate.
     * @param flow Flow rate, relevant for demand-based creators.
     * @param spacing Spacing between vehicles, relevant for state-based creators.
     * @param speed Initial vehicle speed, relevant for state-based creators.
     * @param variability Variability factor, relevant for stochastic creators.
     */
    static void validate_parameters(
        CreatorType type,
        double flow,
        double spacing,
        double speed,
        double variability
    );
};

#endif // CREATOR_FACTORY_H
