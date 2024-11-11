/**
 * @file newell_constrained_timestep.h
 * @author Andres Vial
 * @date 24 May 2022
 * @brief Header file for the newell_constrained_timestep class definition.
 * 
 * @details This class extends the Newell car-following model but constrains the timestep value to always be 1. This ensures consistency in simulations requiring fixed timesteps, as certain models may depend on this behavior.
 */

#ifndef _NEWELL_CONSTRAINED_TIMESTEP
#define _NEWELL_CONSTRAINED_TIMESTEP

#include <math.h>
#include "models/newell.h"
#include "point.h"
#include "clock.h"
#include "exception.h"

/**
 * @class newell_constrained_timestep
 * @brief Newell (2002) car-following model with a constrained timestep of 1.
 * 
 * This class is a variant of the Newell car-following model, with the only difference being that the timestep is validated and fixed to 1. It inherits all properties and functionalities of the original Newell model.
 */
class newell_constrained_timestep : public newell {
public:
    /**
     * @brief Default constructor for the newell_constrained_timestep model.
     * 
     * This constructor initializes the model using default parameters for Newell’s car-following model with the timestep constrained to 1.
     */
    newell_constrained_timestep();

    /**
     * @brief Constructor with custom parameters for Newell's model.
     * 
     * This constructor allows setting custom values for Newell’s car-following model, with the timestep validation constrained to 1.
     * 
     * @param p Pointer to the p_newell parameter class containing model parameters.
     */
    newell_constrained_timestep(p_newell* p);

    /**
     * @brief Validates the model parameters, ensuring the timestep is constrained to 1.
     * 
     * This method ensures that the timestep of the model adheres to the fixed value of 1. If any parameter violates this condition, an exception is raised.
     * 
     * @param p Pointer to the params class containing model parameters.
     */
    void validate_parameters(params* p = nullptr) override;

    /**
     * @brief Computes the next point in the follower's trajectory.
     * 
     * This method calculates the follower’s next position and velocity based on the constrained timestep model.
     * 
     * @param leader Generalized trajectory of the leader vehicle.
     * @param follower Trajectory of the follower vehicle.
     * @param p Parameters for Newell's car-following model.
     * @return A point representing the follower's updated position and speed.
     */
    Point* new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p = nullptr) override;
};

#endif
