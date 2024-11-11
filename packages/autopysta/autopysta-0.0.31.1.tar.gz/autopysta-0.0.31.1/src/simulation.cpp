#include "simulation.h"

bool Clock::is_updated = false;
double Clock::time = 0.0;
double Clock::dt;

#pragma region Constructor
Simulation::Simulation(LCM* lane_change_model, double total_time, Geometry* geometry, Creator* creator, double time_step, bool verbose) {
    if (time_step <= 0) throw Exception(901, "Invalid parameters: time_step should be greater than zero.");
    if (total_time <= 0) throw Exception(901, "Invalid parameters: total_time should be greater than zero.");
    const double epsilon = 1e-9;  // Tolerance for floating-point comparison
    if (std::abs(total_time - std::round(total_time / time_step) * time_step) > epsilon) {
        throw Exception(901, "Invalid parameters: total_time should be a multiple of time_step.");
    }
	Clock::is_updated = false;
	Clock::time = 0.0;
	Clock::dt = time_step;

    this->total_time = total_time;
    this->highway_geometry = geometry;
    this->total_steps = total_time / Clock::dt;
    this->all_vehicles = std::vector<Vehicle*>();
    this->lane_objects = std::vector<std::list<RoadObject*>*>();
    this->lane_change_model = lane_change_model;
    this->current_timestep = 0;
    this->creator_count = highway_geometry->get_initial_lanes();
    this->lane_count = highway_geometry->get_max_lanes();
    this->verbose = verbose;
    this->initialized = false;

    for (int i = 0; i < lane_count; i++) {
        lane_objects.push_back(new std::list<RoadObject*>());
        lane_creators.push_back(creator);
    }
	
    if (highway_geometry->has_merge()) {
        int lane = highway_geometry->get_initial_lanes();
        for (auto x : highway_geometry->get_merge_positions()) {
            merge_end = new FixedObject(new Point(0, x, 0, 0, lane)); 
            insert_vehicle(merge_end);
            lane_creators.push_back(creator);
            if (lane > 1) {  // Ensure lane stays within valid bounds
                lane--;
            }
        }
    }
}

Simulation::Simulation(LCM* lane_change_model, double total_time, Geometry* geometry, std::vector<Creator*> creators, Vehicle* vehicle, double time_step, bool verbose) 
    : Simulation(lane_change_model, total_time, geometry, creators[0], time_step, verbose) {
    overwrite_creators(creators);
    insert_vehicle(vehicle);
    external_vehicle_count = 1;
}

Simulation::Simulation(LCM* lane_change_model, double total_time, Geometry* geometry, std::vector<Creator*> creators, std::vector<Vehicle*> vehicles, double time_step, bool verbose) 
    : Simulation(lane_change_model, total_time, geometry, creators[0], time_step, verbose) {
    overwrite_creators(creators);
    for (auto& vehicle : vehicles) {
        insert_vehicle(vehicle);
    }
    external_vehicle_count = vehicles.size();
}

#pragma endregion

#pragma region Methods
void Simulation::append_vehicle(RoadObject* new_vehicle) {
    int lane_index = new_vehicle->current()->LANE() - 1;

	// Check if the Vehicle lane is a valid one
	if (!test::range_inc(lane_index, 0, lane_count - 1)){
		return;
	}

	// Check if the Vehicle is of type Vehicle and not a FixedObject and add it to "all"
	if (typeid(*new_vehicle) == typeid(Vehicle)){
		all_vehicles.push_back((Vehicle*)new_vehicle);
	}

	// Add the Vehicle to the corresponding lane list of road_objects
	lane_objects[lane_index]->push_back(new_vehicle);
}

void Simulation::append_vehicles(std::vector<Vehicle*> new_vehicles, int lane) {
    int lane_index = lane - 1;

	// Check if the Vehicle lane is a valid one
	if (!test::range_inc(lane_index, 0, lane_count - 1)){
		return;
	}

	// Insert the vehicles at the end of "all"
	all_vehicles.insert(all_vehicles.end(), new_vehicles.begin(), new_vehicles.end());

	// Insert the vehicles at the end of the corresponding lane list of road_objects
	lane_objects[lane_index]->insert(lane_objects[lane_index]->end(), new_vehicles.begin(), new_vehicles.end());
}

void Simulation::insert_vehicle(RoadObject* new_vehicle) {
    
    if (typeid(*new_vehicle) == typeid(Vehicle) && static_cast<Vehicle*>(new_vehicle)->needs_initialization) {
        static_cast<Vehicle*>(new_vehicle)->initialize_vehicle();
	}
    new_vehicle->current()->reset_time();
    int lane_index = new_vehicle->current()->LANE() - 1;

	// Check if the Vehicle lane is a valid one
	if (!test::range_inc(lane_index, 0, lane_count - 1)){
		return;
	}

    // Add to vehicle list if the object is of type Vehicle
    if (typeid(*new_vehicle) == typeid(Vehicle)) {
        all_vehicles.push_back(static_cast<Vehicle*>(new_vehicle));
    }

	// Iterate through the list until the correct index for the Vehicle
    auto it = lane_objects[lane_index]->begin();
    for (; it != lane_objects[lane_index]->end() && (*it)->current()->X() > new_vehicle->current()->X(); ++it);

	// Insert the Vehicle in the lane where it corresponds
    lane_objects[lane_index]->insert(it, new_vehicle);
}

int Simulation::get_current_lane(std::vector<std::list<RoadObject*>::iterator> line, std::vector<std::list<RoadObject*>::iterator> ends) {
    double max_position = -1;
    int lane_index = -1;
    for (int i = 0; i < lane_count; i++) {
        if (line[i] != ends[i] && (*line[i])->current()->X() > max_position) {
            lane_index = i;
            max_position = (*line[i])->current()->X();
        }
    }
    return lane_index;
}

void Simulation::initialize_state(unsigned long seed) {

    std::cout << "Initializing simulation state with Seed: " << seed << std::endl;
    RandomGenerator::init(seed);

    if (verbose) {
        print_debug_initial_state();
    }

    std::vector<Vehicle*> temp_vehicles;
    for (int lane = 0; lane < creator_count; lane++) {
        lane_creators[lane]->validate_creator();
        if (lane_objects[lane]->size() > 0) {
            auto back_element = lane_objects[lane]->back();
            if (typeid(*back_element) != typeid(FixedObject)) {
                temp_vehicles = lane_creators[lane]->initialize_state(back_element->current());
                append_vehicles(temp_vehicles, lane + 1);
            }
        }
    }
    initialized = true;
}

void Simulation::overwrite_creators(std::vector<Creator*> creators) {
    // Check if there are the same number of creators as lanes
    if (creators.size() != static_cast<size_t>(creator_count)) {
        std::cout << creators.size() << " " << creator_count << std::endl;
        throw Exception(901, "Invalid parameters: Number of creators must match number of lanes.");
    }

    // Overwrite creators for lanes
    for (int i = 1; i < creator_count; i++) {
        lane_creators[i] = creators[i];
    }
}

Results* Simulation::run(unsigned long seed) {
    // Initialization section
    if (!initialized) initialize_state(seed);


    const int bar_width = 50;
    RoadObject* leader;

    std::string progress_bar(bar_width, ' ');

    // Unicode block for progress
    const std::string filled_block = "█";
    const std::string empty_block = " "; 

    // Main simulation loop
    for (current_timestep = 0; current_timestep <= total_steps; current_timestep++) { 
        Clock::time = current_timestep * Clock::dt;

        // Update progress bar only at significant changes (every 2%)
        double progress = static_cast<double>(current_timestep) / total_steps;
        int pos = static_cast<int>(bar_width * progress);

        static int last_pos = -1;
        if (pos != last_pos) {  // Update only when there's a visual change
            last_pos = pos;

            // Construct progress bar manually
            std::string current_bar;
            current_bar.reserve(bar_width);  // Avoid reallocations
            for (int i = 0; i < bar_width; ++i) {
                if (i < pos) {
                    current_bar += filled_block;  // Filled part
                } else {
                    current_bar += empty_block;  // Empty part
                }
            }

            fprintf(stdout, "\r[%s] %3d%%", current_bar.c_str(), static_cast<int>(progress * 100));
            fflush(stdout); 
        }

        // Update vehicles
        for (int lane = 0; lane < lane_count; lane++) {

            leader = nullptr;
            for (auto road_object = lane_objects[lane]->begin(); road_object != lane_objects[lane]->end(); road_object++) {
                (*road_object)->update(leader);
                leader = *road_object;
            }

            // Remove vehicle if it has passed the end of the road
            if (lane_objects[lane]->size() > 0 && lane_objects[lane]->front()->current()->X() > highway_geometry->get_length()) {
                lane_objects[lane]->pop_front();
            }
        }

        Clock::is_updated = !Clock::is_updated;

        // Check lane-changes
        std::vector<RoadObject*> lane_leaders(lane_count);
        std::vector<std::list<RoadObject*>::iterator> lane_followers(lane_count);
        std::vector<std::list<RoadObject*>::iterator> lane_ends(lane_count);

        for (int lane = 0; lane < lane_count; lane++) {
            lane_leaders[lane] = nullptr;
            lane_followers[lane] = lane_objects[lane]->begin();
            lane_ends[lane] = lane_objects[lane]->end();
        }

        int current_lane, target_lane, prospective_lane;
        current_lane = get_current_lane(lane_followers, lane_ends);

        while (current_lane != -1) {
            target_lane = current_lane;

            RoadObject* subject = *lane_followers[current_lane];
            Point* subject_position = subject->current();
            Point* left_leader = nullptr;
            Point* right_leader = nullptr;

            // Decide on lane change
            if (typeid(*subject) == typeid(Vehicle) && subject->model != nullptr) {
                if (highway_geometry->can_change_right(subject_position)) {
                    prospective_lane = current_lane + 1;
                    if (lane_leaders[prospective_lane]) left_leader = lane_leaders[prospective_lane]->current();
                    if (lane_followers[prospective_lane] != lane_ends[prospective_lane]) right_leader = (*lane_followers[prospective_lane])->current();
                    if (lane_change_model->lch_right(nullptr, subject_position, left_leader, right_leader, subject->model)) 
                        target_lane = prospective_lane;
                }
                
                if (highway_geometry->can_change_left(subject_position)) {
                    prospective_lane = current_lane - 1;
                    if (lane_leaders[prospective_lane]) left_leader = lane_leaders[prospective_lane]->current();
                    if (lane_followers[prospective_lane] != lane_ends[prospective_lane]) right_leader = (*lane_followers[prospective_lane])->current();
                    if (lane_change_model->lch_left(nullptr, subject_position, left_leader, right_leader, subject->model)) 
                        target_lane = prospective_lane;
                }
            }

            // Perform lane change if necessary
            if (target_lane != current_lane) {
                subject->current()->set_lane(target_lane + 1);
                lane_followers[current_lane] = lane_objects[current_lane]->erase(lane_followers[current_lane]);
                lane_objects[target_lane]->insert(lane_followers[target_lane], subject);
            } else {
                lane_followers[current_lane]++;
            }
            lane_leaders[target_lane] = subject;
            current_lane = get_current_lane(lane_followers, lane_ends);
        }

        // Create new vehicles
        for (int lane = 0; lane < creator_count; lane++) {
            Vehicle* new_vehicle = nullptr;
            if (lane_objects[lane]->size() > 0) {
                RoadObject* last_object = lane_objects[lane]->back();
                if (typeid(*last_object) != typeid(FixedObject)) {
                    new_vehicle = lane_creators[lane]->create(last_object->current());
                } else {
                    new_vehicle = lane_creators[lane]->create_no_leader(lane + 1);
                }
            } else {
                new_vehicle = lane_creators[lane]->create_no_leader(lane + 1);
            }
            if (new_vehicle) {
                append_vehicle(new_vehicle);
            }
        }
    }

    fprintf(stdout, "\n[simulation.cpp] Out of loops, preparing the results.\n");

    // Prepare results
    std::vector<Trajectory*>* result_trajectories = new std::vector<Trajectory*>();
    for (auto& vehicle : all_vehicles) result_trajectories->push_back(static_cast<Trajectory*>(vehicle->trajectory));

    auto results = new Results(result_trajectories);

    // [Experimental Feature]
    // results->export_visualization_data_to_json("visualization_data.json", total_time, Clock::dt, lane_count);

    return results;
}

Simulation::~Simulation() {
    for (auto it = all_vehicles.begin() + external_vehicle_count; it != all_vehicles.end(); it++) {
        delete *it;
    }
    for (auto& lane_object : lane_objects) {
        lane_object->clear();
        delete lane_object;
    }
}


void Simulation::print_debug_initial_state() {
    std::cout << "--- Simulation Overview ---\n";
    std::cout << std::left
              << std::setw(15) << "Total Time"
              << std::setw(15) << "Total Steps"
              << std::setw(15) << "Max Lane Count"
              << std::setw(15) << "Creator Count"
              << std::setw(15) << "Highway Length"
              << std::setw(20) << "Lane Change Model"
              << '\n';

    std::cout << std::setw(15) << total_time
              << std::setw(15) << total_steps
              << std::setw(15) << lane_count
              << std::setw(15) << creator_count
              << std::setw(15) << (highway_geometry ? std::to_string((int)highway_geometry->get_length()) : "N/A")
              << std::setw(20) << (lane_change_model ? typeid(*lane_change_model).name() : "None")
              << '\n';

    std::cout << std::endl;

    std::cout << "---- Highway Overview ----\n";
    highway_geometry->print_highway();

    std::cout << std::endl;
}


#pragma endregion
