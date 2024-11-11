/**
 * @file geometry.h
 * @brief Defines the `Geometry` class for managing highway segment properties in traffic simulations.
 * 
 * @details The `Geometry` class represents the physical characteristics of a simulated highway segment,
 *          including its length, number of lanes, and presence of on/off ramps.
 */

#ifndef GEOMETRY_H
#define GEOMETRY_H

#include "point.h"
#include "exception.h"
#include <algorithm>
#include <vector>
#include <iomanip>
#include <iostream>


class Geometry {
private:
    double length;                    //!< Total length of the highway segment (meters).
    int initial_lanes;                //!< Initial number of lanes at the beginning of the segment.
    int max_lanes;                    //!< Maximum possible lanes at any point on the highway segment.

    // double merge_position; //!< Position from the origin where an on-ramp ends (meters, 0 for no on-ramp).
    // double diverge_position; //!< Position from the origin where an off-ramp starts (meters, >= length for no off-ramp).

    std::vector<double> merge_positions;  //!< Positions along the highway where lanes merge.
    std::vector<double> diverge_positions; //!< Positions along the highway where lanes diverge.


    /**
     * @brief Determines if a lane-changing maneuver is possible.
     *
     * Checks whether a vehicle can change lanes either to the left or the right based on the vehicle's
     * current position and lane, and the geometry of the highway segment.
     *
     * @param point Pointer to the current position of the vehicle.
     * @param to_left Set to `true` for left lane change, `false` for right lane change.
     * @return `true` if the lane change is allowed, `false` otherwise.
     */
	bool can_change_lanes(Point *point, bool to_left) const;

    /**
     * @brief Computes the maximum possible lanes across the highway length based on merges/diverges.
     *
     * Calculates the maximum number of lanes across the highway segment at any position,
     * taking into account all merges and diverges.
     * 
     * @return The maximum number of lanes across the highway.
     */
    int compute_max_lanes() const;

public:
    /**
     * @brief Constructs a `Geometry` object with specified physical properties.
     * 
     * Validates that the highway length and initial lanes are positive.
     * Checks that merge and diverge positions are within the highway’s bounds and sorted in ascending order.
     * Ensures that merges do not reduce lanes below one, and that diverges do not unrealistically increase lane count.
     *
     * @param length Length of the highway segment in meters.
     * @param initial_lanes Initial number of lanes at the start of the segment.
     * @param merge_positions Positions where lanes merge (sorted in ascending order).
     * @param diverge_positions Positions where lanes diverge (sorted in ascending order).
     * @throws Exception if any of the input parameters are invalid.
     */
    Geometry(double length, int initial_lanes, std::vector<double> merge_positions, std::vector<double> diverge_positions);

    /**
     * @brief Constructs a `Geometry` object with specified physical properties.
     *
     * @param length Length of the highway segment in meters.
     * @param initial_lanes Initial number of lanes at the start of the segment.
     * @param merge_position Position where lanes merge.
     * @param diverge_position Positions where lanes diverge.
     * @throws Exception if any of the input parameters are invalid.
     */
    Geometry(double length, int initial_lanes, double merge_position, double diverge_position)
        : Geometry(length, initial_lanes, std::vector<double>{merge_position}, std::vector<double>{diverge_position}) {}

    /**
     * @brief Constructs a `Geometry` object with specified physical properties.
     *
     * @param length Length of the highway segment in meters.
     * @param initial_lanes Initial number of lanes at the start of the segment.
     * @param merge_positions Positions where lanes merge (sorted in ascending order).
     * @param diverge_position Position where a the lanes diverge.
     * @throws Exception if any of the input parameters are invalid.
     */
    Geometry(double length, int initial_lanes, std::vector<double> merge_positions, double diverge_position)
        : Geometry(length, initial_lanes, std::move(merge_positions), std::vector<double>{diverge_position}) {}

    /**
     * @brief Constructs a `Geometry` object with specified physical properties.
     *
     * @param length Length of the highway segment in meters.
     * @param initial_lanes Initial number of lanes at the start of the segment.
     * @param merge_position Position where lanes merge.
     * @param diverge_positions Positions where a the lanes diverge (sorted in ascending order).
     * @throws Exception if any of the input parameters are invalid.
     */
    Geometry(double length, int initial_lanes, double merge_position, std::vector<double> diverge_positions)
        : Geometry(length, initial_lanes, std::vector<double>{merge_position}, std::move(diverge_positions)) {}

    /**
     * @brief Constructs a `Geometry` object with minimal properties (no ramps).
     *
     * @param length Length of the highway segment in meters.
     * @param lanes Number of lanes.
     */
    Geometry(double length, int lanes) : Geometry(length, lanes, {}, {}) {}

    /**
     * @brief Returns the total length of the highway segment.
     *
     * @return The length of the highway in meters.
     */
    double get_length() const;

    /**
     * @brief Returns the initial number of lanes on the highway.
     *
     * @return The total number of lanes (excluding on/off-ramps).
     */
    int get_initial_lanes() const;

    /**
     * @brief Returns the max amount of lanes on the highway
     * 
     * @return returns max_lanes which includes the ammount of merges and diverges
     */
    int get_max_lanes() const;

    /**
     * @brief Returns the current number of lanes based on a given position.
     * @param position The position along the highway segment in meters.
     * @return The current number of lanes.
     */
    int get_current_lanes(double position) const;

    /**
     * @brief Checks if a vehicle can change lanes to the left.
     *
     * @param point Pointer to the current position of the vehicle.
     * @return `true` if a left lane change is allowed, `false` otherwise.
     */
    bool can_change_left(Point *point) const;

    /**
     * @brief Checks if a vehicle can change lanes to the right.
     *
     * @param point Pointer to the current position of the vehicle.
     * @return `true` if a right lane change is allowed, `false` otherwise.
     */
    bool can_change_right(Point *point) const;

    /**
     * @brief Checks if the highway segment has an on-ramp (merge).
     *
     * @return `true` if there is an on-ramp, `false` otherwise.
     */
    bool has_merge() const;

    /**
     * @brief Checks if the highway segment has an off-ramp (diverge).
     *
     * @return `true` if there is an off-ramp, `false` otherwise.
     */
    bool has_diverge() const;

    /**
     * @brief Returns the merge positions along the highway.
     * @return A vector of merge positions in meters.
     */
    const std::vector<double>& get_merge_positions() const;

    /**
     * @brief Returns the diverge positions along the highway.
     * @return A vector of diverge positions in meters.
     */
    const std::vector<double>& get_diverge_positions() const;

    /**
     * @brief Returns the current lane count at a specified position for debugging purposes.
     * @param position The position along the highway.
     * @return The current number of lanes at the given position.
     */
    void print_highway() const;
};

#endif // GEOMETRY_H
