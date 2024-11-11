/**
 * @file martinez_jin_2020.h
 * @author Andres Vial.
 * @date 26 May 2022
 * @brief Header file for the martinez_jin_2020 class definition based on the Martinez and Jin (2020) car-following model.
 * 
 * @details This class implements the Martinez and Jin (2020) car-following model, which is a stochastic extension of Newell's model. 
 * The model introduces a time-gap parameter (`tau`) to represent wave travel time and derives the wave speed (`w`) from this parameter. 
 * It also includes a stochastic jam spacing (`kj`) to account for vehicle heterogeneity in traffic simulations involving autonomous and human-driven vehicles.
 */

#ifndef _MARTINEZ_JIN_2020
#define _MARTINEZ_JIN_2020

#include "params/p_martinez_jin_2020.h"
#include "models/newell_constrained_timestep.h"
#include "point.h"
#include "clock.h"
#include "exception.h"

/**
 * @class martinez_jin_2020
 * @brief Martinez and Jin (2020) car-following model with constrained timestep.
 * 
 * This class implements a stochastic car-following model based on the work of Martinez and Jin (2020), 
 * which extends Newell’s model by incorporating a wave travel time parameter (`tau`) and a stochastic jam density (`kj`).
 * The model accounts for driver heterogeneity, allowing for the inclusion of both autonomous and human-driven vehicles with different dynamic behaviors.
 */
class martinez_jin_2020 : public newell_constrained_timestep {
private:
    /**
     * @brief Initializes the model's wave speed and jam spacing parameters.
     * 
     * This method sets the wave travel time (`tau`) and computes the stochastic jam spacing (`sj`) from the model parameters.
     * 
     * @param p Pointer to the p_martinez_jin_2020 parameter class containing the model parameters.
     */
    void initialize_parameters(p_martinez_jin_2020* p);

public:
    /**
     * @brief Default constructor for the martinez_jin_2020 model.
     * 
     * Initializes the model using default parameters from the p_martinez_jin_2020 class.
     */
    martinez_jin_2020();

    /**
     * @brief Constructor with custom parameter values for the Martinez-Jin model.
     * 
     * This constructor allows initializing the model with custom values for the wave travel time (`tau`) and stochastic jam density (`kj`).
     * 
     * @param p Pointer to the p_martinez_jin_2020 parameter class containing the model parameters.
     */
    martinez_jin_2020(p_martinez_jin_2020* p);
};

#endif
