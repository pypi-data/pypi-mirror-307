/**
 * @file p_newell_random_acceleration.h
 * @date 1 May 2022
 * @brief Header file for the p_newell_random_acceleration class definition.
 * 
 * @details This class extends the p_newell class by adding parameters specific to the random acceleration model of Laval et al. (2014). These parameters include the standard deviation of random acceleration and the inverse relaxation time, controlling the variability in driver behavior.
 */

#ifndef _P_NEWELL_RANDOM_ACCELERATION
#define _P_NEWELL_RANDOM_ACCELERATION

#include "params/p_newell.h"

/**
 * @class p_newell_random_acceleration
 * @brief Parameter class for the random acceleration model based on Laval et al. (2014).
 * 
 * This class manages the specific parameters required for Laval's random acceleration extension to Newell's car-following model. These parameters control the stochastic behavior of vehicles in traffic simulations.
 */
class p_newell_random_acceleration : public p_newell {
public:
    double sigma_tilde = 0.11; //!< Standard deviation of the random acceleration term.
    double beta = 0.07;        //!< Inverse relaxation time, affecting the temporal responsiveness of vehicles.

    /**
     * @brief Default constructor for the random acceleration parameters.
     * 
     * Initializes the parameters with default values based on typical traffic conditions.
     */
    p_newell_random_acceleration();

    /**
     * @brief Constructor with custom parameter values.
     * 
     * This constructor allows setting custom values for the standard deviation (`sigma_tilde`), inverse relaxation time (`beta`), as well as inherited parameters from p_newell.
     * 
     * @param u Free-flow speed in meters per second.
     * @param w Wave speed in meters per second.
     * @param kj Jam density in vehicles per meter.
     * @param sigma_tilde Standard deviation of the random acceleration term.
     * @param beta Inverse relaxation time.
     */
    p_newell_random_acceleration(double u, double w, double kj, double sigma_tilde, double beta);
};

#endif
