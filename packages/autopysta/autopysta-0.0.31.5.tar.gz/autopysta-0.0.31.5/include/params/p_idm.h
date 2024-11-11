/**
 * @file p_idm.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Parameters for the Intelligent Driver Model (IDM).
 * 
 * @details This file defines the class for IDM-specific parameters, including maximum speed, 
 * desired time headway, and vehicle acceleration characteristics. These parameters are based 
 * on the model proposed by Treiber, Hennecke, and Helbing (2000) to simulate traffic congestion 
 * dynamics.
 * 
 * @see M. Treiber, A. Hennecke, and D. Helbing, "Congested traffic states in empirical observations 
 * and microscopic simulations," Phys. Rev. E, 62, 1805 (2000).
 */

#ifndef _P_IDM_H
#define _P_IDM_H

#include "params/params.h"
#include "exception.h"

/**
 * @class p_idm
 * @brief Parameters for the Intelligent Driver Model (IDM).
 * 
 * This class contains the specific parameters for the Intelligent Driver Model (IDM), including 
 * maximum desired speed, acceleration and deceleration capabilities, and desired time headway.
 * These parameters control the behavior of vehicles in the IDM and can be tuned based on empirical data.
 */
class p_idm : public params {
public:
    double v0 = 120.0 / 3.6; //!< Maximum desired speed (m/s).
    double T = 1.6;          //!< Desired time headway (s).
    double a = 0.73;         //!< Maximum acceleration (m/s²).
    double b = 1.67;         //!< Comfortable deceleration (m/s²).
    double dl = 4;           //!< Acceleration exponent.
    double s0 = 2;           //!< Minimum gap (jam distance) in congested traffic (m).
    double l = 5;            //!< Vehicle length (m).

    /**
     * @brief Default constructor with standard IDM parameters.
     * 
     * Initializes the IDM parameters with default values based on empirical studies.
     * 
     * @see M. Treiber, A. Hennecke, and D. Helbing, "Congested traffic states in empirical observations 
     * and microscopic simulations," Phys. Rev. E, 62, 1805 (2000).
     */
    p_idm();

    /**
     * @brief Constructor for IDM parameters with custom values.
     * 
     * This constructor allows the user to define custom values for the IDM parameters, including 
     * maximum speed, time headway, and acceleration properties.
     * 
     * @param v0 Maximum desired speed (m/s).
     * @param T Desired time headway (s).
     * @param a Maximum acceleration (m/s²).
     * @param b Comfortable deceleration (m/s²).
     * @param s0 Minimum gap in congested traffic (m).
     * @param l Vehicle length (m).
     */
    p_idm(double v0, double T, double a, double b, double s0, double l);
};

#endif // _P_IDM_H
