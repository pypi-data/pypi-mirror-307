/**
 * @file newell_random_acceleration.h
 * @date 1 May 2022
 * @author Andres Vial
 * @brief Header file for the newell_random_acceleration class definition.
 * 
 * @details This class is an extension of the Newell car-following model based on the work by Laval et al. (2014). The model introduces random acceleration behavior, incorporating driver variability with additional parameters such as standard deviation of acceleration.
 */

#ifndef _NEWELL_RANDOM_ACCELERATION
#define _NEWELL_RANDOM_ACCELERATION

#include "params/p_newell_random_acceleration.h"
#include "models/newell.h"
#include <math.h>
#include <algorithm>
#include "point.h"
#include "clock.h"
#include "exception.h"
#include "random_generator.h"

/**
 * @class newell_random_acceleration
 * @brief Laval et al. (2014) car-following model with random acceleration behavior.
 * 
 * This class implements a variant of Newell’s car-following model that includes random acceleration dynamics, as introduced by Laval et al. (2014). The model captures variability in driver behavior, incorporating stochastic fluctuations in vehicle acceleration.
 */
class newell_random_acceleration : public newell {
private:
    float ksi_std_dev; //!< Standard deviation of the random acceleration term (ksi).

    /**
     * @brief Initializes model parameters specific to the random acceleration model.
     * 
     * This function sets up the parameters for random acceleration behavior in Laval's model, including the standard deviation for random fluctuations.
     * 
     * @param p Pointer to the p_newell_random_acceleration class containing the model parameters.
     */
	void initialize_parameters(p_newell_random_acceleration* p);

public:
    /**
     * @brief Default constructor for the random acceleration model.
     * 
     * Initializes the model using default values for both Newell’s and Laval’s model parameters, including random acceleration settings.
     */
	newell_random_acceleration();

    /**
     * @brief Constructor with custom parameters for Newell's and Laval's models.
     * 
     * This constructor allows initializing the model with custom values for both Newell’s car-following parameters and Laval's random acceleration model parameters.
     * 
     * @param p Pointer to the p_newell_random_acceleration class containing the parameters.
     */
	newell_random_acceleration(p_newell_random_acceleration* p);

    /**
     * @brief Validates the model parameters for consistency.
     * 
     * This method checks the parameters for both Newell's and Laval’s models to ensure they meet the required conditions.
     * 
     * @param p Pointer to the params class containing model parameters.
     */
    void validate_parameters(params* p = (params*)nullptr) override;

    /**
     * @brief Computes the next point in the follower's trajectory considering random acceleration.
     * 
     * This method calculates the follower's next position and velocity, incorporating the random acceleration behavior introduced by Laval's model.
     * 
     * @param leader Generalized trajectory representing the leader's position and speed int time. Leave null for no leader.
     * @param follower Trajectory representing the follower's position and speed in time. Leave null for no follower.
     * @param p Parameters for Laval’s car-following model.
     * @return A point representing the follower's updated position and speed.
     */
    Point* new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p = (params*)nullptr) override;
};
#endif
