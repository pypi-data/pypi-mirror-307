#include "creators/creator_martinez_jin_2020.h"

CreatorMartinezJin2020::CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed) {
    this->parameters = model_params;
    vehicle_spacing = spacing;
    initial_vehicle_speed = speed;
    initialize_parameters();
}

CreatorMartinezJin2020::CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed, double deviation, double avg_jam_density)
    : CreatorMartinezJin2020(model_params, spacing, speed)
{
    jam_density_deviation = deviation;
    average_jam_density = avg_jam_density;
    initialize_parameters();
}

CreatorMartinezJin2020::CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed, int max_vehicles) 
    : CreatorMartinezJin2020(model_params, spacing, speed)
{
    this->max_vehicles = max_vehicles;
    initialize_parameters();
}

CreatorMartinezJin2020::CreatorMartinezJin2020(p_martinez_jin_2020* model_params, double spacing, double speed, double deviation, double avg_jam_density, int max_vehicles) 
    : CreatorMartinezJin2020(model_params, spacing, speed)
{
    jam_density_deviation = deviation;
    average_jam_density = avg_jam_density;
    this->max_vehicles = max_vehicles;
    initialize_parameters();
}

void CreatorMartinezJin2020::initialize_parameters()
{
    min_jam_density = average_jam_density * (1 - jam_density_deviation);
    max_jam_density = average_jam_density * (1 + jam_density_deviation);
    if (vehicle_spacing <= 0 || vehicle_spacing < (1.0 / max_jam_density)) 
        throw Exception(901, "Wrong parameters. Creator's spacing can't be negative, zero, or less than jam spacing.");
}

Vehicle* CreatorMartinezJin2020::create(Point* leader, bool immediate_follower) {
    if (vehicle_count >= max_vehicles) return nullptr;
    martinez_jin_2020* random_model = create_random_model_instance();
    Point* ideal_conditions = calculate_ideal_conditions(leader);
    double equilibrium_spacing = random_model->equil_spcg(leader->V(), ideal_conditions->V());
    double new_position = leader->X() - equilibrium_spacing;
    if (new_position > ideal_conditions->X()) new_position = ideal_conditions->X();
    if (new_position >= 0) {
        if (!immediate_follower) ideal_conditions->set_x(0);
        vehicle_count++;
        return new Vehicle(random_model, ideal_conditions);    
    } else {
        delete ideal_conditions;
        return nullptr;
    }
}

martinez_jin_2020* CreatorMartinezJin2020::create_random_model_instance() {
    p_martinez_jin_2020* model_params = new p_martinez_jin_2020(parameters->u, parameters->tau);
    double random_jam_density = RandomGenerator::uniform(min_jam_density, max_jam_density);
    model_params->kj = random_jam_density;
    model_params->w = 1.0 / (model_params->kj * model_params->tau);
    martinez_jin_2020* model = new martinez_jin_2020(model_params);
    return model;
}

Point* CreatorMartinezJin2020::calculate_ideal_conditions(Point* leader) {
    return new Point(leader->T(), leader->X() - vehicle_spacing, initial_vehicle_speed, 0, leader->LANE());
}

Vehicle* CreatorMartinezJin2020::create_no_leader(int lane) {
    if (vehicle_count >= max_vehicles) return nullptr;
    vehicle_count++;
    martinez_jin_2020* random_model = create_random_model_instance();
    return new Vehicle(random_model, 0, initial_vehicle_speed, lane);
}

void CreatorMartinezJin2020::validate_creator() {
    p_martinez_jin_2020* model_params = new p_martinez_jin_2020(parameters->u, parameters->tau);
    martinez_jin_2020* model = new martinez_jin_2020(model_params);
    model->validate_parameters();
    delete model;
    delete model_params;
}
