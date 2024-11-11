#include "creators/fixed_state_creator.h"

FixedStateCreator::FixedStateCreator(Model* model, double spacing, double speed) {
    traffic_model = model;
    target_spacing = spacing;
    initial_speed = speed;
    if (target_spacing <= 0 || target_spacing < model->equil_spcg(0, 0)) 
        throw Exception(901, "Wrong parameters. Fixed state creator's spacing can't be negative, zero, or less than jam spacing.");
}

FixedStateCreator::FixedStateCreator(Model* model, double spacing, double speed, int max_vehicles) 
    : FixedStateCreator(model, spacing, speed) {
    this->max_vehicles = max_vehicles;
}


void FixedStateCreator::validate_creator() {
    traffic_model->validate_parameters();
}

Point* FixedStateCreator::calculate_ideal_conditions(Point* leader) {
    return new Point(
        leader->T(), 
        leader->X() - target_spacing, 
        initial_speed, 
        0, 
        leader->LANE()
    );
}

Vehicle* FixedStateCreator::create_no_leader(int lane) {
    if (vehicle_count >= max_vehicles) return nullptr;
    vehicle_count++;
    return new Vehicle(traffic_model, 0, initial_speed, lane);
}
