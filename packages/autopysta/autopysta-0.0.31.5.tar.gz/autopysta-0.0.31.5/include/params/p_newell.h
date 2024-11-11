/**
 * @file p_newell.h
 * @author Rafael Delpiano
 * @date 11 Dec 2019
 * @brief Header file for the p_newell class definition.
 *
 * @details This file defines the p_newell class, which is used to manage the parameters 
 * for Newell's car-following model. These parameters include free-flow speed, wave speed, 
 * and jam density, which are essential for simulating vehicle behavior in traffic.
 */

#ifndef _P_NEWELL
#define _P_NEWELL

#include "params/params.h"
#include "exception.h"

/**
 * @brief Parameter class for Newell's car-following model.
 *
 * The p_newell class manages the specific parameters required for Newell's car-following model. 
 * These parameters control the behavior of vehicles in free-flow and congested traffic conditions.
 *
 * Key Parameters:
 * - Free-flow speed (`u`): The speed at which vehicles travel under free-flow conditions 
 *   (i.e., no congestion). This is typically set in meters per second.
 * - Wave speed (`w`): The speed at which congestion waves propagate backward through the 
 *   traffic. This helps simulate how quickly disturbances in the flow of traffic spread.
 * - Jam density (`kj`): The density of vehicles in a jammed traffic condition, which helps
 *   define the minimum spacing between vehicles.
 */
class p_newell : public params {
public:
    double u = 90.0 / 3.6; //!< Free-flow speed in meters per second (default: 90 km/h).
    double w = 18.0 / 3.6; //!< Wave speed in meters per second (default: 18 km/h).
    double kj = 0.15;      //!< Jam density in vehicles per meter (default: 0.15 vehicles/meter).

    /**
     * @brief Default constructor for p_newell.
     * 
     * Initializes the parameters with default values for free-flow speed, wave speed, 
     * and jam density. These defaults represent typical traffic conditions.
     * 
     * Default Values:
     * - Free-flow speed: 90 km/h
     * - Wave speed: 18 km/h
     * - Jam density: 0.15 vehicles per meter
     */
    p_newell();

    /**
     * @brief Constructor with custom parameter values.
     * 
     * This constructor allows setting custom values for free-flow speed (`u`), wave speed (`w`), 
     * and jam density (`kj`). These values can be used to simulate specific traffic scenarios.
     * 
     * @param u Free-flow speed in meters per second.
     * @param w Wave speed in meters per second.
     * @param kj Jam density in vehicles per meter.
     */
    p_newell(double u, double w, double kj);
};

#endif
