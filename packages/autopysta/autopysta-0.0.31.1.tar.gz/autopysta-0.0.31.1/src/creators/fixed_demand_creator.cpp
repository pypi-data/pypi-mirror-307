#include "creators/fixed_demand_creator.h"
#include <algorithm>

FixedDemandCreator::FixedDemandCreator(Model* model, double flow) {
    traffic_model = model;
    flow_rate = flow;
    vehicle_headway = 1 / flow;
}

FixedDemandCreator::FixedDemandCreator(Model* model, double flow, int max_vehicles) 
    : FixedDemandCreator(model, flow) {
    this->max_vehicles = max_vehicles;
}


void FixedDemandCreator::validate_creator() {
    if (flow_rate > 1 / Clock::dt) {
        throw Exception(901, "Wrong parameters. Unfeasible Demand (flow < 1/dt)");
    }
    traffic_model->validate_parameters();
}

Point* FixedDemandCreator::calculate_ideal_conditions(Point* leader) {
    double leader_speed = leader->V();

    return new Point(
        leader->T(), 
        leader->X() - std::max(vehicle_headway * leader_speed, traffic_model->equil_spcg(leader_speed, leader_speed)), 
        leader_speed, 
        0, 
        leader->LANE()
    );
}

Vehicle* FixedDemandCreator::create_no_leader(int lane) {
    if (vehicle_count >= max_vehicles) return nullptr;
    vehicle_count++;
    return new Vehicle(traffic_model, 0, traffic_model->free_flow_speed(), lane);
}
