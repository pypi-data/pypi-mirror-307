/**
 * @file vehicle.h
 * @author Rafael Delpiano.
 * @date 11 Dec 2019
 * @brief Defines the `RoadObject`, `vehicle`, and `FixedObject` classes used to represent objects on the road.
 *
 * @details This file contains the definitions for the `RoadObject` class and its derived classes, `vehicle` and `FixedObject`.
 *          These classes are used to model moving vehicles and static objects on a road, along with their trajectories.
 *          The `vehicle` class provides multiple constructors for defining vehicles based on different types of input such as
 *          position history or models.
 */

#ifndef _VEH
#define _VEH

#include "models/model.h"
#include "models/example_car.h"
#include "point.h"
#include "trajectory.h"
#include "exception.h"
#include <queue>

/**
 * @brief Abstract base class representing any object on the road.
 *
 * The `RoadObject` class serves as a general interface for objects on the road, whether they are moving vehicles or fixed objects.
 * It handles the object's trajectory and allows updating based on interactions with other road objects.
 */
class RoadObject {
public:
    Model* model = nullptr; //!< Pointer to the model associated with the object (optional).
    GeneralizedTrajectory* trajectory = nullptr; //!< Object's trajectory, which defines its movement and positions over time.
    std::queue<Point*> defined_t; //!< A queue of defined trajectory points provided by the user.

    /**
     * @brief Virtual destructor for the `RoadObject` class.
     */
    virtual ~RoadObject() {}

    /**
     * @brief Get the current point of the object.
     * 
     * This pure virtual function must be implemented by derived classes to return the object's current position and state.
     * 
     * @return A pointer to the current point representing the object's state.
     */
    virtual Point* current() const = 0;

    /**
     * @brief Update the object's state based on another road object.
     *
     * This pure virtual function must be implemented by derived classes. It updates the object’s state, such as position and speed,
     * possibly considering the position of a leader or other objects on the road.
     *
     * @param leader A pointer to the road object that may influence this object’s state.
     */
    virtual void update(RoadObject* leader) = 0;
};

/**
 * @brief Class representing a moving vehicle on the road.
 *
 * The `vehicle` class models a moving vehicle, which can either follow a predefined trajectory or behave according to a dynamic model.
 * It offers multiple constructors to accommodate different ways of specifying the vehicle’s movement, including position history,
 * points, or models that dictate its behavior.
 */
class Vehicle : public RoadObject {
private:
    /**
     * @brief Initialize placeholder points for the vehicle based on historical positions and lanes.
     *
     * This function sets up a queue of placeholder points that contain position (X) and lane information. These points
     * serve as placeholders until they are updated with real values during the simulation.
     *
     * @param hist_X A vector of X positions representing the vehicle's position over time.
     * @param lanes A vector of lane positions corresponding to each X position.
     */
    void set_empty_points_queue(std::vector<double> hist_X, std::vector<int> lanes);

    /**
     * @brief Update the vehicle with a new point.
     *
     * This method updates the vehicle's position and state with a new point during the simulation.
     *
     * @param new_point Pointer to the new point that updates the vehicle’s position.
     */
    void update(Point* new_point);

    /**
     * @brief Validate the time delta (dt) between the current point and the new point.
     *
     * This method ensures that the time difference between the current point and the new point matches the simulation's delta time.
     * 
     * @param new_point A pointer to the new point being added.
     * @throws Exception If the time delta between points does not match the expected delta time.
     */
    void check_dt(Point* new_point);

public:
    bool needs_initialization = false; //!< Flag indicating if the vehicle requires initialization within the simulation.
    std::vector<Point*> placeholder_points; //!< A vector of placeholder points used before simulation starts.

    /**
     * @brief Create a vehicle with a predefined trajectory and a single lane.
     *
     * This constructor initializes a vehicle with a list of X positions and a single lane. It assumes that the positions are
     * equally spaced in time, with a fixed delta time between points.
     *
     * @param x A vector of X positions representing the vehicle’s position over time.
     * @param l The lane in which the vehicle is moving.
     */
    Vehicle(std::vector<double> x, int l);

    /**
     * @brief Create a vehicle with a predefined trajectory across multiple lanes.
     *
     * This constructor initializes a vehicle with a list of X positions and a list of lane positions.
     * It assumes that the positions are equally spaced in time, with a fixed delta time between points.
     *
     * @param x A vector of X positions representing the vehicle’s position over time.
     * @param l A vector of lane positions corresponding to each X position.
     * @throws Exception If the size of `x` and `l` do not match.
     */
    Vehicle(std::vector<double> x, std::vector<int> l);

    /**
     * @brief Create a vehicle with a predefined trajectory based on points.
     *
     * This constructor initializes a vehicle with a list of `point` objects that define its trajectory over time.
     *
     * @param p A vector of pointers to `point` objects representing the vehicle's trajectory.
     * @throws Exception If the size of the trajectory is too short.
     */
    Vehicle(std::vector<Point*> p);

    /**
     * @brief Create a vehicle with a model, initial position, speed, and lane.
     *
     * This constructor initializes a vehicle with a dynamic model that dictates its behavior, along with its initial position,
     * speed, and lane.
     *
     * @param model Pointer to the model that will describe the vehicle's behavior.
     * @param position The initial position of the vehicle.
     * @param speed The initial speed of the vehicle.
     * @param lane The lane in which the vehicle starts.
     */
    Vehicle(Model* model, double position, double speed, int lane);

    /**
     * @brief Create a vehicle with a model and a starting point.
     *
     * This constructor initializes a vehicle with a dynamic model and a starting point, which contains information about its
     * position, speed, and lane.
     *
     * @param model Pointer to the model that will describe the vehicle's behavior.
     * @param point Pointer to the initial point of the vehicle.
     */
    Vehicle(Model* model, Point* point);

    /**
     * @brief Initialize the vehicle’s trajectory with real points.
     *
     * This method initializes the placeholder points of a vehicle that was created with a predefined trajectory,
     * replacing them with real points in the simulation.
     */
    void initialize_vehicle();

    /**
     * @brief Get the model parameters associated with the vehicle.
     *
     * @return A pointer to the model parameters (`params`).
     */
    params* p();

    /**
     * @brief Get the current point of the vehicle.
     *
     * This method returns the vehicle's current position and state based on its trajectory.
     *
     * @return A pointer to the current point.
     */
    Point* current() const override;

    /**
     * @brief Update the vehicle's state based on a leader vehicle.
     *
     * This method updates the vehicle's state (position, speed, etc.) based on the trajectory of a leading vehicle.
     * If no leader is provided, the vehicle's state is updated according to its model or predefined trajectory.
     *
     * @param leader A pointer to the road object acting as the leader vehicle.
     * @throws Exception If the vehicle runs out of predefined points for the simulation.
     */
    void update(RoadObject* leader) override;

    /**
     * @brief Destructor for the `vehicle` class.
     *
     * Cleans up dynamically allocated memory associated with the vehicle's trajectory.
     */
    ~Vehicle();
};

/**
 * @brief Class representing a fixed object on the road.
 *
 * The `FixedObject` class models a static object on the road, such as a roadblock or a parked vehicle. 
 * It remains stationary and has a fixed position in the simulation.
 */
class FixedObject : public RoadObject {
    Point* pos; //!< The fixed position of the object.

public:
    /**
     * @brief Constructor for the `FixedObject` class.
     *
     * Initializes the object with a fixed position on the road.
     *
     * @param pos A pointer to the position of the object.
     */
    FixedObject(Point* pos);

    /**
     * @brief Get the current position of the fixed object.
     *
     * Since the object is fixed, this method always returns the same position.
     *
     * @return A pointer to the object's current position.
     */
    Point* current() const override;

    /**
     * @brief Update the state of the fixed object.
     *
     * Since the object is fixed, this method does nothing. It is provided to satisfy the interface.
     *
     * @param ro A pointer to another road object (unused in this context).
     */
    void update(RoadObject* ro) override;
};

#endif
