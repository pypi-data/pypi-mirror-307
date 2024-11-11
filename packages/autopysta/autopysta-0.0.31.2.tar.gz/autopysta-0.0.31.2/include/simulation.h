/**
 * @file simulation.h
 * @version 0.1
 * @date 06/09/2019
 * @author Rafael Delpiano.
 * @title 2D Traffic Model Simulation
 * 
 * @brief This file contains the definitions for the `simulation` class.
 * @details The `simulation` class manages the entire traffic simulation process.
 * It handles vehicle creation, updating, and lane changes, based on different 
 * lane-changing models and vehicle dynamics.
 */

#ifndef SIMULATION_H
#define SIMULATION_H

#include "params/params.h"
#include "models/model.h"
#include "creators/creator.h"

#include "utils/profiler.h"

#include <iostream>
#include <typeinfo>
#include <iomanip> 
#include <vector>
#include <string>
#include <list>

#include "point.h"
#include "trajectory.h"
#include "vehicle.h"
#include "geometry.h"
#include "clock.h"
#include "misc.h"
#include "results.h"
#include "exception.h"
#include "random_generator.h"

/**
 * @brief The `simulation` class manages a traffic simulation over time.
 * 
 * This class controls the creation of vehicles, their movement, lane changes, 
 * and interactions on a highway-like scenario. It updates vehicle states in 
 * discrete time steps.
 */
class Simulation {
private:
    LCM* lane_change_model;                             //!< Lane-change model for the simulation.
    double total_time;                                  //!< Total simulation time in seconds.
    Geometry* highway_geometry;                         //!< Geometry of the highway.
    std::vector<Creator*> lane_creators;                //!< List of vehicle creators for each lane.
    int current_timestep = 0;                           //!< Current step of the simulation.
    int total_steps;                                    //!< Total number of simulation steps (total_time / time_step_).
    int external_vehicle_count = 0;                     //!< Number of externally provided vehicles.
    std::vector<Vehicle*> all_vehicles;                 //!< List of all vehicles in the simulation.
    std::vector<std::list<RoadObject*>*> lane_objects;  //!< List of road objects (vehicles, obstacles) per lane.
    int creator_count;                                  //!< Number of vehicle creators (usually equal to the number of lanes).
    int lane_count;                                     //!< Number of lanes in the simulation.
    FixedObject* merge_end;                             //!< Fixed object at the end of a merge lane.
    bool initialized = false;                           //!< Indicates whether the simulation has been initialized.
    bool verbose = false;                            //!< Flag to control debug mode for verbose output.


    /**
     * @brief Adds a new vehicle to the simulation.
     * 
     * This method adds a road object (usually a vehicle) to the simulation.
     * It assigns the object to the correct lane.
     * 
     * @param new_vehicle A pointer to the new vehicle to be added.
     */
    void append_vehicle(RoadObject* new_vehicle);

    /**
     * @brief Adds multiple vehicles to a specific lane.
     * 
     * The vehicles are inserted into the specified lane and the simulation's 
     * internal list of vehicles is updated accordingly.
     * 
     * @param vehicles Vector of vehicles to be added.
     * @param lane Lane number where the vehicles will be added.
     */
    void append_vehicles(std::vector<Vehicle*> vehicles, int lane);

    /**
     * @brief Inserts a vehicle into the correct position in its lane.
     * 
     * The vehicle is inserted in order, based on its position on the road.
     * 
     * @param vehicle A pointer to the vehicle to be inserted.
     */
    void insert_vehicle(RoadObject* vehicle);

    /**
     * @brief Retrieves the current lane with the furthest advanced vehicle.
     * 
     * This method checks which lane currently has the vehicle furthest down 
     * the road, used during the lane change checks.
     * 
     * @param line Iterators pointing to the current vehicles in each lane.
     * @param ends Iterators pointing to the end of each lane.
     * @return The index of the lane with the furthest vehicle.
     */
    int get_current_lane(std::vector<std::list<RoadObject*>::iterator> line, std::vector<std::list<RoadObject*>::iterator> ends);

    /**
     * @brief Initializes the simulation state.
     * 
     * This method initializes the simulation by creating the initial state 
     * of each lane.
     */
    void initialize_state(unsigned long seed);

    /**
     * @brief Overwrites the default lane creators with the provided ones.
     * 
     * This method allows the simulation to use specific vehicle creators 
     * for each lane, overwriting the default creator used during initialization.
     * 
     * @param creators A std::vector of vehicle creators, one for each lane.
     */
    void overwrite_creators(std::vector<Creator*> creators);

    /**
     * @brief Helper function used to print the initial state of a simulation
     * 
     * Only ran when the debug_mode flag is set to true
     */
    void print_debug_initial_state();
public:
    /**
     * @brief Constructs a simulation with a common creator for all lanes.
     * 
     * @param lane_change_model Lane-changing model.
     * @param total_time Total simulation time.
     * @param geometry Highway geometry.
     * @param creator Vehicle creator for all lanes.
     * @param time_step Time step for the simulation.
     * @param verbose flag to enable verbose mode that prints some aditional info
     */
    Simulation(LCM* lane_change_model, double total_time, Geometry* geometry, Creator* creator, double time_step, bool verbose = false);

    /**
     * @brief Constructs a simulation with specific creators for each lane.
     * 
     * @param lane_change_model Lane-changing model.
     * @param total_time Total simulation time.
     * @param geometry Highway geometry.
     * @param creators Vector of vehicle creators for each lane.
     * @param vehicle A specific vehicle to insert into the simulation.
     * @param time_step Time step for the simulation.
     * @param verbose flag to enable verbose mode that prints some aditional info
     */
    Simulation(LCM* lane_change_model, double total_time, Geometry* geometry, std::vector<Creator*> creators, Vehicle* vehicle, double time_step, bool verbose = false);

    /**
     * @brief Constructs a simulation with specific creators and vehicles.
     * 
     * @param lane_change_model Lane-changing model.
     * @param total_time Total simulation time.
     * @param geometry Highway geometry.
     * @param creators Vector of vehicle creators for each lane.
     * @param vehicles Vector of pre-existing vehicles to insert into the simulation.
     * @param time_step Time step for the simulation.
     * @param verbose flag to enable verbose mode that prints some aditional info
     */
    Simulation(LCM* lane_change_model, double total_time, Geometry* geometry, std::vector<Creator*> creators, std::vector<Vehicle*> vehicles, double time_step, bool verbose = false);

    /**
     * @brief Runs the simulation.
     * 
     * This method runs the simulation, advancing the simulation state step 
     * by step until completion.
     * 
     * @return A pointer to a `results` object containing the simulation results.
     */
    Results* run(unsigned long seed = static_cast<unsigned long>(std::time(nullptr)));

    /**
     * @brief Destructor for the simulation.
     * 
     * Cleans up all dynamically allocated memory used by the simulation.
     */
    ~Simulation();
};

#endif
