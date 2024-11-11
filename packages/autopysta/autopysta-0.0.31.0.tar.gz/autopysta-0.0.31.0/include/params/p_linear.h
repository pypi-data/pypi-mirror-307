/**
 * @file p_linear.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Header file for the p_linear class definition.
 *
 * @details This file defines the parameters used by the linear car-following model. These parameters control the
 * behavior of vehicles, such as their desired speed, reaction time, and spacing.
 */

#ifndef _P_LINEAR_H
#define _P_LINEAR_H

#include "params/params.h"
#include "exception.h"

/**
 * @brief Parameter class for the linear car-following model.
 *
 * This class stores the parameters used in the linear car-following model. These parameters include:
 * 
 * - Free-flow speed (V): The desired speed when no vehicles are ahead.
 * - Coefficients (c1, c2, c3): Constants that control the sensitivity to speed and spacing differences.
 * - Jam spacing (sr): The minimum distance maintained between vehicles when stopped.
 * - Reaction time (tau): The time it takes for the driver to react to changes in the vehicle ahead.
 * 
 * These parameters are essential for simulating vehicle behavior in traffic flow.
 */
class p_linear : public params {
public:
    double V = 120 / 3.6;    //!< Free-flow speed in m/s (default value: 120 km/h).
    double c1 = 1.0 / 20.0;  //!< Coefficient for speed difference sensitivity.
    double c2 = 93.0 / 160.0; //!< Coefficient for follower's speed difference sensitivity.
    double c3 = 9.0 / 64.0;  //!< Coefficient for spacing sensitivity.
    double sr = 220.0 / 9;   //!< Jam spacing (minimum distance between vehicles when stopped).
    double tau = 4.0 / 6;    //!< Driver's reaction time in seconds.

    //! Default constructor for p_linear.
    /*!
     * Initializes the parameters with default values based on typical traffic conditions:
     * Free-flow speed = 120 km/h, reaction time = 4/6 seconds, and default coefficients for speed and spacing.
     */
    p_linear();

    //! Constructor with custom parameter values.
    /*!
     * This constructor allows setting custom values for the linear model parameters.
     * 
     * \param V Free-flow speed in m/s.
     * \param c1 Coefficient for speed difference sensitivity.
     * \param c2 Coefficient for follower's speed difference sensitivity.
     * \param c3 Coefficient for spacing sensitivity.
     * \param sr Jam spacing in meters.
     * \param tau Driver's reaction time in seconds.
     */
    p_linear(double V, double c1, double c2, double c3, double sr, double tau);
};

#endif
