/**
 * @file p_martinez_jin_2020.h
 * @author Andres Vial.
 * @date 11 Dec 2019
 * @brief Header file for the p_martinez_jin_2020 class definition.
 * 
 * @details This class manages the parameters for the stochastic LWR car-following model based on the work by Martinez and Jin (2020). 
 * The model introduces stochasticity in vehicle parameters, including jam density, and is specifically designed to account for heterogeneous traffic flow, 
 * such as the presence of autonomous and human-driven vehicles with different jam densities and time gaps.
 */

#ifndef _P_MARTINEZ_JIN_2020
#define _P_MARTINEZ_JIN_2020

#include "params/p_newell.h"

/**
 * @class p_martinez_jin_2020
 * @brief Parameter class for Martinez and Jin (2020) stochastic car-following model.
 * 
 * This class defines the parameters for the Martinez and Jin (2020) model, an extension of Newell's car-following theory. 
 * The model accounts for heterogeneous driver behavior by introducing a wave travel time parameter (`tau`) and stochastic jam density.
 */
class p_martinez_jin_2020 : public p_newell {
public:
    double tau = 1.5;       //!< Wave travel time (τ), controlling the delay in vehicle reactions to changes in traffic.
    
    /**
     * @brief Default constructor for the p_martinez_jin_2020 parameter class.
     * 
     * Initializes the model with default values for wave travel time (`tau`) and inherited parameters from the Newell model.
     */
    p_martinez_jin_2020();

    /**
     * @brief Constructor with custom parameter values.
     * 
     * Allows setting custom values for the free-flow speed (`u`) and wave travel time (`tau`).
     * 
     * @param u Free-flow speed in meters per second.
     * @param tau Wave travel time in seconds.
     */
    p_martinez_jin_2020(double u, double tau);
};

#endif
