#include "results.h"
#include <vector>
#include <stdexcept> // For exception handling


#pragma region Results class

Results::Results(std::vector<Trajectory*>* trajectories) {
    all_trajectories = trajectories;
    lane_map = nullptr;
}


Trajectory* Results::get_trajectory(std::size_t index) {
    if (index >= all_trajectories->size()) {
        throw std::out_of_range("Index out of range in Results::get_trajectory");
    }
    return all_trajectories->at(index);
}

void Results::classify() {
	lane_map = new std::map<int, std::vector<Trajectory*>*>();
	for (std::size_t c = 0; c < all_trajectories->size(); c++) {
		Trajectory* trajectory = all_trajectories->at(c);
        int current_lane = trajectory->at(0)->LANE();
        Trajectory* lane_trajectory = new Trajectory(trajectory->at(0));

        for (int point_index = 1; point_index < trajectory->get_trajectory_length(); ++point_index) {
            Point* point = trajectory->at(point_index);
            if (point->LANE() != current_lane) {
				add_t_to_lanes(current_lane, lane_trajectory);
                current_lane = point->LANE();
                lane_trajectory = new Trajectory(point);
			}
			else {
                lane_trajectory->push_back(point);
			}
		}
		add_t_to_lanes(current_lane, lane_trajectory);
	}
}

void Results::add_t_to_lanes(int lane, Trajectory* trajectory) {
    if (lane_map->count(lane) > 0) {
        lane_map->at(lane)->push_back(trajectory);
	}
	else {
        auto* new_trajectory_list = new std::vector<Trajectory*>();
        new_trajectory_list->push_back(trajectory);
        lane_map->insert({lane, new_trajectory_list});
	}
}

std::vector<Trajectory*>* Results::get_trajectories_by_vehicle(int vehicle_index) {
    Trajectory* trajectory = all_trajectories->at(vehicle_index);
    Point* initial_point = trajectory->get_point_at(0);
    int current_lane = initial_point->LANE();
    auto* result = new std::vector<Trajectory*>();
    Trajectory* lane_trajectory = new Trajectory(initial_point);

    for (int i = 1; i < trajectory->get_trajectory_length(); ++i) {
        initial_point = trajectory->get_point_at(i);
        if (initial_point->LANE() != current_lane) {
            result->push_back(lane_trajectory);
            current_lane = initial_point->LANE();
            lane_trajectory = new Trajectory(initial_point);
        } else {
            lane_trajectory->push_back(initial_point);
        }
	}
    result->push_back(lane_trajectory);
    return result;
}

std::vector<Trajectory*>* Results::get_trajectories_by_lane(int lane) {
    if (lane_map == nullptr) {
        classify();
    }
	// In case that l doesn't exist in lanes:
    if (lane_map->find(lane) == lane_map->end()) {
        return new std::vector<Trajectory*>();
    }
    return lane_map->at(lane);
}

std::vector<Trajectory*>* Results::get_all_trajectories_by_lane() {
	if (lane_map == nullptr) {
		classify();
	}
    auto* result = new std::vector<Trajectory*>();
    for (auto& lane_entry : *lane_map) {
        for (auto* trajectory : *(lane_entry.second)) {
            result->push_back(trajectory);
        }
    }
    return result;
}

std::vector<Trajectory*>* Results::get_all_trajectories() {
	return all_trajectories;
}

std::vector<std::vector<double>*>* Results::calculate_box_edges(double start_time, double end_time, double time_step) {
    auto* intervals = new std::vector<std::vector<double>*>();
    int num_intervals = (end_time - start_time) / time_step;
    time_step = (end_time - start_time) / num_intervals;
    for (int i = 0; i < num_intervals; ++i) {
        intervals->push_back(new std::vector<double>{ start_time, start_time + time_step });
        start_time += time_step;
    }
	return intervals;
}

std::vector<std::vector<double>*>* Results::calculate_edie(double start_time, double end_time, double time_step, double start_dist, double end_dist, int lane) {
	if (lane_map == nullptr) {
		classify();
	}

    auto* result = new std::vector<std::vector<double>*>();
    auto* box_list = new std::vector<Box*>();
    auto* box_edges = calculate_box_edges(start_time, end_time, time_step);
    
    for (auto* edge : *box_edges) {
        box_list->push_back(new Box(start_dist, end_dist, edge->at(0), edge->at(1)));
    }

    for (auto* trajectory : *lane_map->at(lane)) {
        for (auto* box : *box_list) {
            if (box->trails->back()->at(0)->T() != -1) {
                box->trails->push_back(new std::vector<Point*>{ new Point(-1, -1, 0, 0, 0), new Point(-1, -1, 0, 0, 0) });
            }
		}
        for (std::size_t point_index = 0; point_index < trajectory->size(); ++point_index) {
            Point* point = trajectory->at(point_index);
            for (auto* box : *box_list) {
                if (box->contains(point)) {
                    if (box->trails->back()->at(0)->T() == -1) {
                        box->trails->back()->at(0) = new Point(*point);
                        if (point_index > 0) {
                            Point* previous_point = trajectory->at(point_index - 1);
                            if (!box->contains(previous_point)) {
                                Point* mid_point = box->get_intersection(previous_point, point);
                                if (box->contains(mid_point)) {
                                    box->trails->back()->at(0) = new Point(*mid_point);
                                }
							}
						}
					}
                    if (point->T() >= box->trails->back()->at(1)->T()) {
                        box->trails->back()->at(1) = new Point(*point);
                        if (point_index + 1 < trajectory->size()) {
                            Point* next_point = trajectory->at(point_index + 1);
                            if (!box->contains(next_point)) {
                                Point* mid_point = box->get_intersection(point, next_point);
                                if (box->contains(mid_point)) {
                                    box->trails->back()->at(1) = new Point(*mid_point);
                                }
							}
						}
					}
					
				}
			}
		}
	}
    for (auto* box : *box_list) {
        std::vector<double>* flow_density = box->get_edie();
        result->push_back(flow_density);
    }
	return result;
}

std::vector<Point*>* Results::passes_on_t(double time, int lane) {
    auto* result = new std::vector<Point*>();
	//fprintf(stderr, "Lanes length %d\n", lanes->size());
    for (auto* trajectory : *lane_map->at(lane)) {
		//fprintf(stderr, "Trajectory %d length: %d\n", t_i, trayectory->size());
        if (trajectory->size() > 1) {
            Point* start_point = trajectory->at(0);
            Point* end_point = trajectory->at(1);
            std::size_t point_index = 2;
            while (end_point->T() <= time && point_index < trajectory->size()) {
                start_point = end_point;
                end_point = trajectory->at(point_index);
                ++point_index;
            }
            if (start_point->T() <= time && time <= end_point->T()) {
                double time_ratio = time - start_point->T();
                double interpolated_x = start_point->X() + time_ratio * start_point->V();
                double interpolated_v = start_point->V() + time_ratio * start_point->A();
                double interpolated_a = start_point->A();
                result->push_back(new Point(time, interpolated_x, interpolated_v, interpolated_a, lane));
            }
		}
	}
    return result;
}

std::vector<Point*>* Results::passes_on_x(double position, int lane) {
    auto* result = new std::vector<Point*>();
	//fprintf(stderr, "Lanes length %d\n", lanes->size());
    for (auto* trajectory : *lane_map->at(lane)) {
		//fprintf(stderr, "Trajectory %d length: %d\n", t_i, trayectoria->size());
        if (trajectory->size() > 1) {
            Point* start_point = trajectory->at(0);
            Point* end_point = trajectory->at(1);
            std::size_t point_index = 2;
            while (end_point->X() <= position && point_index < trajectory->size()) {
                start_point = end_point;
                end_point = trajectory->at(point_index);
                ++point_index;
            }
            if (start_point->X() <= position && position <= end_point->X()) {
                double time_at_position = (position - start_point->X()) * (end_point->T() - start_point->T()) / (end_point->X() - start_point->X()) + start_point->T();
                double time_ratio = time_at_position - start_point->T();
                double interpolated_v = start_point->V() + time_ratio * start_point->A();
                double interpolated_a = start_point->A();
                result->push_back(new Point(time_at_position, position, interpolated_v, interpolated_a, lane));
            }
        }
	}

    return result;
}

#pragma endregion

#pragma region Box class

Box::Box(double x_start, double x_end, double t_start, double t_end) {
    x_min = x_start;
    x_max = x_end;
    t_min = t_start;
    t_max = t_end;
    trails = new std::vector<std::vector<Point*>*>{ new std::vector<Point*>{ new Point(-1, -1, 0, 0, 0), new Point(-1, -1, 0, 0, 0) }};
    A = (t_max - t_min) * (x_max - x_min);
}

bool Box::contains(Point* point) const {
    return point->X() >= x_min && point->X() <= x_max && point->T() >= t_min && point->T() <= t_max;
}

Point* Box::get_intersection(Point* p1, Point* p2) {
	double t = -1;
	double x = -1;
	// Case 1
	if (p1->X() <= x_min && t_max <= p1->T() && p1->T() <= t_max && contains(p2)) {
		t = (x_min - p1->X()) * (p2->T() - p1->T()) / (p2->X() - p1->X()) + p1->T();
		x = x_min;
	}
	//Case 2
	else if (contains(p1) && x_max <= p2->X() && t_max <= p2->T() && p2->T() <= t_max) {
		t = (x_max - p1->X()) * (p2->T() - p1->T()) / (p2->X() - p1->X()) + p1->T();
		x = x_max;
	}
	//Case 3
	else if (p1->X() <= x_min
			&& p1->T() <= t_max
			&& contains(p2)) {
		Point* mid = inter_hor(p1, p2, x_min);
		if (!(mid->T() >= t_max)) {
			mid = inter_ver(p1, p2, t_max);
		}
		t = mid->T();
		x = mid->X();
	}
	//Case 4
	else if (contains(p1)
			&& t_max <= p2->T() 
			&& x_max <= p2->X()) {
		Point* mid = inter_hor(p1, p2, x_max);
		if (!(mid->T() >= t_max)) {
			mid = inter_ver(p1, p2, t_max);
		}
		t = mid->T();
		x = mid->X();
	}
	//Case 5
	else if (x_min <= p1->X() && p1->X() <= x_max && p1->T() <= t_max && contains(p2)){
		Point* mid = inter_ver(p1, p2, t_max);
		t = mid->T();
		x = mid->X();
	}
	//Case 6
	else if (contains(p1) && x_min <= p2->X() && p2->X() <= x_max && t_max <= p2->T()){
		Point* mid = inter_ver(p1, p2, t_max);
		t = mid->T();
		x = mid->X();
	}
	return new Point(t, x, 0, 0, p1->LANE());
}

Point* Box::inter_hor(Point* p1, Point* p2, double x) {
	double t = (x - p1->X()) * (p2->T() - p1->T()) / (p2->X() - p1->X()) + p1->T();
	return new Point(t, x, 0, 0, p1->LANE());
}

Point* Box::inter_ver(Point* p1, Point* p2, double t) {
	double x = (t - p1->T())*(p2->X() - p1->X())/(p2->T() - p1->T()) + p1->X();
	return new Point(t, x, 0, 0, p1->LANE());
}

std::vector<double>* Box::get_edie() {
    double total_distance = 0;
    double total_time = 0;

    for (auto* trail : *trails) {
        total_distance += trail->at(1)->X() - trail->at(0)->X();
        total_time += trail->at(1)->T() - trail->at(0)->T();
    }
    return new std::vector<double>{ total_distance / A, total_time / A };
}

void Box::print() const {
    fprintf(stderr, "Trails:\n");
    for (auto* trail : *trails) {
        fprintf(stderr, "   [%f, %f] > [%f, %f]\n",
                trail->at(0)->T(), trail->at(0)->X(),
                trail->at(1)->T(), trail->at(1)->X());
    }
}
#pragma endregion


// Agregar trys: Resultado de la simulación
