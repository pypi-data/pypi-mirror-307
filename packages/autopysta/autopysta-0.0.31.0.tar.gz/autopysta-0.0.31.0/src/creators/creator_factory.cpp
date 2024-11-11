#include "creators/creator_factory.h"


Creator* CreatorFactory::create_creator(
    CreatorType type,
    Model* model,
    double flow,
    int max_vehicles,
    double spacing,
    double speed,
    double variability
) {
    validate_parameters(type, flow, spacing, speed, variability);

    Creator* creator = nullptr;
    switch (type) {
        case FixedDemand:
            creator = new FixedDemandCreator(model, flow, max_vehicles);
            break;

        case FixedState:
            creator = new FixedStateCreator(model, spacing, speed, max_vehicles);
            break;

        default:
            throw std::invalid_argument("Invalid creator type specified.");
    }
    return creator;
}

void CreatorFactory::validate_parameters(
    CreatorType type,
    double flow,
    double spacing,
    double speed,
    double variability
) {
    switch (type) {
        case FixedDemand:
            if (flow <= 0) throw std::invalid_argument("Flow rate must be positive for FixedDemand creator.");
            break;

        case FixedState:
            if (spacing <= 0) throw std::invalid_argument("Spacing must be positive for FixedState creator.");
            if (speed < 0) throw std::invalid_argument("Speed must be non-negative for FixedState creator.");
            break;

        default:
            throw std::invalid_argument("Unknown creator type.");
    }
}
