/**
 * @file clock.h
 * @author Rafael Delpiano
 * @date unknown
 * @brief File for the clock class definition (short description).
 *
 * @details This file contains the definition of the `Clock` class, which provides a 
 * centralized means of tracking and advancing time in the simulation.
 * The class is used to manage the global simulation time and synchronize 
 * updates across other components.
 */

#ifndef _CLOCK
#define _CLOCK

/**
 * @class Clock
 * @brief Manages and synchronizes time within the simulation.
 * 
 * The `Clock` class contains static variables for tracking the simulation's 
 * global time (`time`), the fixed time interval (`dt`) between updates, and 
 * an update flag (`isUpdated`) to indicate the current state of time progression. 
 * 
 * This class allows the simulation to keep a consistent notion of time that can 
 * be referenced and modified as needed by other components, such as vehicle 
 * dynamics, lane changes, and position updates.
 */
class Clock {
public:
    static double time;       //!< The current global simulation time, in seconds.
    static double dt;         //!< The fixed time step, in seconds, used to advance `time` at each update.
    static bool is_updated;    //!< A flag indicating the current update state, used to synchronize changes.
};

#endif
