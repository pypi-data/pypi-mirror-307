#include "creators/creator.h"

void Creator::validate_creator() {}

Vehicle* Creator::create(Point* leader, bool immediate_follower) {
    if (vehicle_count >= max_vehicles) return nullptr;

    Point* ideal_conditions = calculate_ideal_conditions(leader);
    double equilibrium_spacing = traffic_model->equil_spcg(leader->V(), ideal_conditions->V());
    double new_position = leader->X() - equilibrium_spacing;

    if (new_position > ideal_conditions->X()) {
        new_position = ideal_conditions->X();
    }

    if (new_position >= 0) {
        if (!immediate_follower) {
            ideal_conditions->set_x(0);
        }
        vehicle_count++;
        return new Vehicle(traffic_model, ideal_conditions);    
    } else {
        delete ideal_conditions;
        return nullptr;
    }
}

std::vector<Vehicle*> Creator::initialize_state(Point* leader) {
    std::vector<Vehicle*> vehicles;
    Vehicle* next_vehicle = this->create(leader, true);

    while (next_vehicle != nullptr) {
        vehicles.push_back(next_vehicle);
        next_vehicle = this->create(vehicles.back()->current(), true);
    }

    return vehicles;
}
