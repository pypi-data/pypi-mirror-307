/**
 * @file results.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Defines the `results` and `Box` classes for managing simulation results.
 *
 * @details This file contains the implementation of the `results` class, which manages 
 * simulation data, and the `Box` class, which defines a time-space region for measuring Edie's values.
 */

#ifndef _RESULTS
#define _RESULTS

#include "trajectory.h"
#include <map>
#include <vector>
#include <fstream>
#include <iostream>



/**
 * @brief The `results` class manages and processes simulation results.
 *
 * This class stores and organizes the trajectories of vehicles by lane, and provides methods 
 * to analyze the data, such as computing Edie's flow and density, or getting vehicle positions at 
 * specific times or distances.
 */
class Results {
private:
    std::vector<Trajectory*>* all_trajectories; //!< Stores trajectories of all vehicles in the simulation.
    std::map<int, std::vector<Trajectory*>*>* lane_map; //!< Map of lanes, where each lane is associated with a list of trajectories.

    /**
     * @brief Adds a Trajectory to the corresponding lane in the `lanes` map.
     *
     * @param lane Lane corresponding to the Trajectory.
     * @param trajectory Trajectory to be added.
     */
    void add_t_to_lanes(int lane, Trajectory* trajectory);

    /**
     * @brief Classifies and organizes trajectories by lane.
     *
     * This function iterates through all trajectories, breaking them up by lane changes 
     * and storing them in the `lanes` map.
     * 
     *      lane (key)	trajectories (value)
     *      1		    { [p1, p2, p3], [p1, p2, p3], ..., [p1, p2] }
     *      2		    { [p1, p2, p3], [p1, p2, p3], ..., [p1, p2] }
     *      ...         ...
     *      n		    { [p1, p2, p3], [p1, p2, p3], ..., [p1, p2] }
     * 
     */
    void classify();

    /**
     * @brief Creates box edges for measuring Edie's values within specific time intervals.
     *
     * @param start_time Start time.
     * @param end_time End time.
     * @param time_step Time step size.
     * @return A vector of vectors representing the edges of the boxes.
     */
    std::vector<std::vector<double>*>* calculate_box_edges(double start_time, double end_time, double time_step);

public:
    /**
     * @brief Constructor that initializes the `results` object with a list of trajectories.
     *
     * @param trajectories A vector of trajectories from the simulation.
     */
    Results(std::vector<Trajectory*>* trajectories);

    Trajectory* get_trajectory(std::size_t index);

    /**
     * @brief Splits a vehicle's Trajectory by lane.
     *
     * This method processes the Trajectory of a specific vehicle and splits it into 
     * separate trajectories based on lane changes.
     *
     * @param vehicle_index Index of the vehicle Trajectory.
     * @return A vector of trajectories split by lane.
     */
    std::vector<Trajectory*>* get_trajectories_by_vehicle(int vehicle_index);

    /**
     * @brief Retrieves all trajectories in a specific lane.
     *
     * @param lane Lane number.
     * @return A vector of trajectories in the specified lane.
     */
    std::vector<Trajectory*>* get_trajectories_by_lane(int lane);

    /**
     * @brief Retrieves all trajectories across all lanes.
     *
     * @return A vector containing all trajectories in the simulation.
     */
    std::vector<Trajectory*>* get_all_trajectories_by_lane();

    /**
     * @brief Gets all vehicle trajectories.
     *
     * @return A vector containing the trajectories of all vehicles.
     */
    std::vector<Trajectory*>* get_all_trajectories();

    /**
     * @brief Computes Edie's flow and density for a specific time interval and distance.
     *
     * This method analyzes the Trajectory data to calculate flow and density values 
     * within a specified time-space region.
     *
     * @param start_time Start time.
     * @param end_time End time.
     * @param time_step Time step size.
     * @param start_dist Start distance.
     * @param end_dist End distance.
     * @param lane Lane number.
     * @return A vector of vectors containing the computed flow and density values.
     */
    std::vector<std::vector<double>*>* calculate_edie(double start_time, double end_time, double time_step, double start_dist, double end_dist, int lane);

    /**
     * @brief Retrieves the list of points where vehicles pass at a specific time in a given lane.
     *
     * @param time The time at which to check vehicle positions.
     * @param lane The lane number.
     * @return A vector of points representing vehicle positions at the specified time and lane.
     */
    std::vector<Point*>* passes_on_t(double time, int lane);

    /**
     * @brief Retrieves the list of points where vehicles pass at a specific distance in a given lane.
     *
     * @param position The distance at which to check vehicle positions.
     * @param lane The lane number.
     * @return A vector of points representing vehicle positions at the specified distance and lane.
     */
    std::vector<Point*>* passes_on_x(double position, int lane);
};

/**
 * @brief The `Box` class defines a time-space region for measuring Edie's flow and density.
 *
 * A `Box` is a rectangular area in time and space used to calculate flow and density values based on
 * the vehicle trajectories that pass through it.
 */
class Box {
private:
    double x_min; //!< Lower bound of the distance range (x-axis).
    double x_max; //!< Upper bound of the distance range (x-axis).
    double t_min; //!< Lower bound of the time range (t-axis).
    double t_max; //!< Upper bound of the time range (t-axis).
    double A; //!< The area of the box in time-space.

public:
    std::vector<std::vector<Point*>*>* trails; //!< Stores the start and end points of trajectories crossing the box.

    /**
     * @brief Constructor that defines a time-space box for measuring flow and density.
     *
     * @param xa Lower bound of the distance range.
     * @param xb Upper bound of the distance range.
     * @param ta Lower bound of the time range.
     * @param tb Upper bound of the time range.
     */
    Box(double xa, double xb, double ta, double tb);

    /**
     * @brief Checks whether a point lies within the box.
     *
     * @param p The point to check.
     * @return `true` if the point is inside the box, `false` otherwise.
     */
    bool contains(Point* p) const;

    /**
     * @brief Computes the intersection of two points with the edges of the box.
     *
     * This method calculates the intersection point of a line segment defined by two points 
     * (p1, p2) with the edges of the box.
     *
     * @param p1 First point of the line segment.
     * @param p2 Second point of the line segment.
     * @return The point of intersection with the box edges.
     */
    Point* get_intersection(Point* p1, Point* p2);

    /**
     * @brief Calculates the intersection with a horizontal line at a given x value.
     *
     * @param p1 First point of the line segment.
     * @param p2 Second point of the line segment.
     * @param x The x-coordinate of the horizontal line.
     * @return The intersection point.
     */
    Point* inter_hor(Point* p1, Point* p2, double x);

    /**
     * @brief Calculates the intersection with a vertical line at a given t value.
     *
     * @param p1 First point of the line segment.
     * @param p2 Second point of the line segment.
     * @param t The t-coordinate of the vertical line.
     * @return The intersection point.
     */
    Point* inter_ver(Point* p1, Point* p2, double t);

    /**
     * @brief Computes Edie's flow and density values for the box.
     *
     * @return A vector containing flow (Q) and density (K) values for the box.
     */
    std::vector<double>* get_edie();

    /**
     * @brief Prints the trails (vehicle paths) that pass through the box.
     *
     * This is used for debugging and visualization purposes.
     */
    void print() const;
};

#endif
