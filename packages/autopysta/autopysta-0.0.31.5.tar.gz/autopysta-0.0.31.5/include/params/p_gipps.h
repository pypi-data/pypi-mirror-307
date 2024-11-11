/**
 * @file p_gipps.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Header file for the p_gipps parameter class definition.
 *
 * @details This file defines the p_gipps class, which stores parameters used in the Gipps car-following model.
 * These parameters represent key behavioral aspects of drivers, such as maximum acceleration, desired speed,
 * reaction time, and braking characteristics.
 */

#ifndef _P_GIPPS_H
#define _P_GIPPS_H

#include "params/params.h"
#include "exception.h"

/**
 * @brief Parameter class for the Gipps car-following model.
 *
 * This class stores the parameters required for simulating vehicle behavior in the Gipps car-following model. 
 * The parameters represent key driver behaviors and vehicle constraints, such as:
 * 
 * - an: Maximum acceleration that the driver is willing to undertake.
 * 
 * - bn: Maximum deceleration (braking) that the driver considers safe.
 * 
 * - sn: Jam spacing, the minimum distance the driver maintains when the vehicle is stopped.
 * 
 * - vn: Free-flow speed, the desired speed when no vehicles are ahead.
 * 
 * - tau: Reaction time, the time it takes for the driver to respond to the vehicle ahead.
 * 
 * - bg: Leader's estimated maximum deceleration, used to predict the worst-case scenario for sudden braking.
 * 
 * These parameters are essential for reproducing realistic traffic behavior in simulations, such as maintaining safe 
 * following distances and appropriate speed adjustments in response to changing traffic conditions.
 * 
 * Reference: Gipps, P.G. (1981), "A Behavioural Car-Following Model for Computer Simulation", 
 * Transport Research Part B, Vol. 15, pp. 105-111.
 */
class p_gipps: public params {
public:
    double an = 1.7;            //!< Maximum acceleration in m/s².
    double bn = -3.4;           //!< Maximum deceleration (braking) in m/s².
    double sn = 6.5;            //!< Jam spacing in meters (the minimum safe distance between stopped vehicles).
    double vn = 120.0 / 3.6;    //!< Free-flow speed in m/s (default value: 120 km/h).
    double tau = 0.8;           //!< Driver's reaction time in seconds.
    double bg = -3.2;           //!< Estimated maximum deceleration of the leader in m/s².

    //! Default constructor for p_gipps.
    /*!
     * Initializes the parameters with default values based on general traffic conditions:
     * an = 1.7 m/s² (maximum acceleration),
     * bn = -3.4 m/s² (maximum deceleration),
     * sn = 6.5 meters (jam spacing),
     * vn = 120 km/h (free-flow speed),
     * tau = 0.8 seconds (reaction time),
     * bg = -3.2 m/s² (leader's estimated maximum deceleration).
     */
    p_gipps();

    //! Constructor with custom parameter values.
    /*!
     * This constructor allows initializing the parameters with custom values, allowing for specific 
     * scenarios to be modeled. These parameters correspond directly to driver and vehicle behaviors.
     * 
     * @param an  Maximum acceleration in m/s².
     * @param bn  Maximum deceleration (braking) in m/s².
     * @param sn  Jam spacing in meters.
     * @param vn  Free-flow speed in m/s.
     * @param tau Reaction time in seconds.
     * @param bg  Leader's estimated maximum deceleration in m/s².
     */
    p_gipps(double an, double bn, double sn, double vn, double tau, double bg);
};

#endif
