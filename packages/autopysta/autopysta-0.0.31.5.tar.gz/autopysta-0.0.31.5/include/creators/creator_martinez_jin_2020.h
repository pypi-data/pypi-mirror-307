/**
 * @file creator_martinez_jin_2020.h
 * @author Andres Vial.
 * @date 19 May 2022
 * @brief Defines the `creator_martinez_jin_2020` class for generating vehicles using the Martinez and Jin (2020) model.
 *
 * @details This class creates vehicles with random jam densities based on the Martinez and Jin (2020) model.
 *          It allows generating vehicles with a fixed spacing and initial speed, while introducing variability in the jam density.
 */

#ifndef _CREATOR_MARTINEZ_JIN_2020
#define _CREATOR_MARTINEZ_JIN_2020

#include "params/p_martinez_jin_2020.h"
#include "models/martinez_jin_2020.h"
#include "creators/creator.h"
#include "random_generator.h"
#include "vehicle.h"


/**
 * @brief Vehicle creator based on the Martinez and Jin (2020) model, with random jam density.
 *
 * The `creator_martinez_jin_2020` class generates vehicles according to the Martinez and Jin (2020) car-following model,
 * with random variations in jam density. Vehicles are placed in a lane with a given spacing and initial speed, unless constrained
 * by the lane's capacity or other vehicles.
 */
class CreatorMartinezJin2020 : public Creator {
private:
    double jam_density_deviation = 0.5; //!< Maximum percentage deviation for random jam density.
    double average_jam_density = 0.14;  //!< Average jam density.
    double vehicle_spacing;             //!< Spacing between consecutive vehicles.
    double initial_vehicle_speed;       //!< Initial speed for the created vehicles.
    p_martinez_jin_2020* parameters;    //!< Parameters for the Martinez and Jin model.

    /**
     * @brief Computes the ideal conditions for creating a new vehicle.
     *
     * This function calculates the optimal starting point and state for a new vehicle based on the
     * current state of the leader vehicle.
     *
     * @param leader A pointer to the current leader vehicle's point.
     * @return A point representing the ideal state for the new vehicle.
     */
    Point* calculate_ideal_conditions(Point* leader) override;

    /**
     * @brief Initializes parameters for the random jam density.
     *
     * This method sets the minimum (`a`) and maximum (`b`) jam density values based on the average jam density (`avg_kj`)
     * and percentage deviation (`ksi`).
     */
    void initialize_parameters();

    /**
     * @brief Creates a new Martinez and Jin model instance with a random jam density.
     *
     * This function generates a new instance of the Martinez and Jin model using random jam density values.
     *
     * @return A new `martinez_jin_2020` model instance.
     */
    martinez_jin_2020* create_random_model_instance();

public:
    double min_jam_density;  //!< Minimum value for random jam density (uniform distribution).
    double max_jam_density;  //!< Maximum value for random jam density (uniform distribution).

    /**
     * @brief Constructs a vehicle creator with the Martinez and Jin model.
     *
     * This constructor creates a vehicle creator that generates vehicles with a fixed spacing and initial speed.
     * Jam density is randomly generated within a defined range.
     *
     * @param model_params Parameters for the Martinez and Jin model.
     * @param spacing Desired spacing between vehicles.
     * @param speed Initial speed for the created vehicles.
     */
    CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed);

    /**
     * @brief Constructs a vehicle creator with the Martinez and Jin model and custom jam density range.
     *
     * This constructor creates a vehicle creator that generates vehicles with a fixed spacing and initial speed.
     * Jam density is randomly generated within the specified range.
     *
     * @param model_params Parameters for the Martinez and Jin model.
     * @param spacing Desired spacing between vehicles.
     * @param speed Initial speed for the created vehicles.
     * @param deviation Maximum percentage deviation for the random jam density.
     * @param avg_jam_density Average jam density.
     */
    CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed, double deviation, double avg_jam_density);

    /**
     * @brief Constructs a vehicle creator with a limit on the number of vehicles.
     *
     * This constructor creates a vehicle creator that generates vehicles with a fixed spacing and initial speed, up to a 
     * maximum number of vehicles.
     *
     * @param model_params Parameters for the Martinez and Jin model.
     * @param spacing Desired spacing between vehicles.
     * @param speed Initial speed for the created vehicles.
     * @param max_vehicles Maximum number of vehicles to be created.
     */
    CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed, int max_vehicles);

    /**
     * @brief Constructs a vehicle creator with a custom jam density range and vehicle limit.
     *
     * This constructor creates a vehicle creator that generates vehicles with a fixed spacing and initial speed, 
     * with a random jam density and a limit on the total number of vehicles created.
     *
     * @param model_params Parameters for the Martinez and Jin model.
     * @param spacing Desired spacing between vehicles.
     * @param speed Initial speed for the created vehicles.
     * @param deviation Maximum percentage deviation for the random jam density.
     * @param avg_jam_density Average jam density.
     * @param max_vehicles Maximum number of vehicles to be created.
     */
    CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed, double deviation, double avg_jam_density, int max_vehicles);

    /**
     * @brief Creates a vehicle with random jam density behind a leader.
     *
     * This method checks whether it is possible to create a vehicle based on the leader's current state. If allowed,
     * it creates a new vehicle using the Martinez and Jin model with random jam density.
     *
     * @param leader The current point of the leader vehicle.
     * @param immediate_follower If `true`, the new vehicle is placed just behind the leader.
     * @return A pointer to the created vehicle, or `nullptr` if no vehicle was created.
     */
    Vehicle* create(Point* leader, bool immediate_follower = false) override;

    /**
     * @brief Creates a vehicle in an empty lane with random jam density.
     *
     * This method generates a vehicle at the start of an empty lane using the Martinez and Jin model with random jam density.
     *
     * @param lane The lane number where the vehicle is created.
     * @return A pointer to the created vehicle, or `nullptr` if no vehicle was created.
     */
    Vehicle* create_no_leader(int lane) override;

    /**
     * @brief Validates the parameters of the Martinez and Jin model.
     *
     * This method ensures that the parameters of the Martinez and Jin model are valid and feasible for the simulation.
     */
    void validate_creator() override;
};

#endif
