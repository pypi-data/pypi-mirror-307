#include "geometry.h"

Geometry::Geometry(double length, int initial_lanes, std::vector<double> merge_positions, std::vector<double> diverge_positions)
    : length(length), initial_lanes(initial_lanes), merge_positions(std::move(merge_positions)), diverge_positions(std::move(diverge_positions)) {
    
    // Validation checks
    if (length <= 0 || initial_lanes <= 0) 
        throw Exception(901, "Invalid parameters: length and lanes should be greater than zero.");

    // Ensure merge and diverge positions are sorted in ascending order
    if (!std::is_sorted(this->merge_positions.begin(), this->merge_positions.end()) || 
        !std::is_sorted(this->diverge_positions.begin(), this->diverge_positions.end())) {
        throw Exception(901, "Merge and diverge positions must be sorted in ascending order.");
    }

    // Check that all merge and diverge positions are within highway bounds
    if (!this->merge_positions.empty() && this->merge_positions.back() >= length) 
        throw Exception(901, "Invalid parameters: merge positions must be within highway length.");
    if (!this->diverge_positions.empty() && this->diverge_positions.back() >= length) 
        throw Exception(901, "Invalid parameters: diverge positions must be within highway length.");

    // Ensure merges do not reduce lanes below 1 at any position
    int min_lanes = initial_lanes - static_cast<int>(this->merge_positions.size());
    if (min_lanes < 1) 
        throw Exception(901, "Invalid configuration: merges would reduce lanes below 1.");

    max_lanes = compute_max_lanes();
}

double Geometry::get_length() const {
    return length;
}

int Geometry::get_initial_lanes() const {
    return initial_lanes;
}

int Geometry::get_max_lanes() const { 
    return max_lanes; 
}

int Geometry::compute_max_lanes() const {
    int current_lanes = initial_lanes;
    int max_lanes = current_lanes;

    // Merge and diverge indices
    size_t merge_index = 0;
    size_t diverge_index = 0;

    // Traverse both merge and diverge positions
    while (merge_index < merge_positions.size() || diverge_index < diverge_positions.size()) {
        if (diverge_index < diverge_positions.size() &&
            (merge_index >= merge_positions.size() || diverge_positions[diverge_index] <= merge_positions[merge_index])) {
            // Diverge at this position
            current_lanes++;
            diverge_index++;
        } else {
            // Merge at this position
            current_lanes--;
            merge_index++;
        }

        // Update the maximum lane count encountered
        max_lanes = std::max(max_lanes, current_lanes);
    }

    return max_lanes;
}

int Geometry::get_current_lanes(double position) const {
    int lanes = initial_lanes;

    // Count merges and diverges that occur before the current position
    int merges = std::upper_bound(merge_positions.begin(), merge_positions.end(), position) - merge_positions.begin();
    int diverges = std::upper_bound(diverge_positions.begin(), diverge_positions.end(), position) - diverge_positions.begin();

    // Calculate the current numberof  lanes
    lanes = initial_lanes - merges + diverges;

    // Ensure lanes are within bounds [1, max_lanes]
    return std::clamp(lanes, 1, max_lanes);
}

bool Geometry::can_change_lanes(Point* point, bool to_left) const {
    int current_lanes = get_current_lanes(point->X());

    if (to_left && point->LANE() <= 1) return false;
    if (!to_left && point->LANE() >= current_lanes) return false;
    if (point->X() >= length) return false;

    return true;
}


bool Geometry::can_change_left(Point *point) const {
    return can_change_lanes(point, true);
}

bool Geometry::can_change_right(Point *point) const {
    return can_change_lanes(point, false);
}

bool Geometry::has_merge() const {
    return !merge_positions.empty();
}

bool Geometry::has_diverge() const {
    return !diverge_positions.empty();
}

const std::vector<double>& Geometry::get_merge_positions() const {
    return merge_positions; 
}

const std::vector<double>& Geometry::get_diverge_positions() const {
    return diverge_positions; 
}



void Geometry::print_highway() const {
    const int display_length = 90; // Number of segments to visually display the highway length
    const char lane_char = '-';    // Standard lane segment
    const char merge_char = '/';   // Mark merge point
    const char diverge_char = '\\'; // Mark diverge point
    const int max_display_lanes = std::min(max_lanes, 10); // Max lanes to show

    // Calculate scaling factor to map highway length to display length
    double scale = length / display_length;

    // Create a header row to mark the beginning and end of the highway
    std::cout << "0m ";
    for (int i = 1; i <= display_length; ++i) {
        if (i == display_length) {
            std::cout << std::setw(3) << static_cast<int>(length) << "m";
        } else {
            std::cout << " "; // Spacing between position markers
        }
    }
    std::cout << "\n";

    // Draw each lane, segment by segment
    for (int lane = 1; lane <= max_display_lanes; ++lane) {
        std::cout << "L" << lane << " |"; // Lane label
        for (int i = 1; i <= display_length; ++i) {
            double pos = i * scale;
            int current_lanes = get_current_lanes(pos);

            // Check if the current lane exists at this position
            if (lane <= current_lanes) {
                if (std::find(merge_positions.begin(), merge_positions.end(), pos) != merge_positions.end()) {
                    std::cout << merge_char; // Mark merge point
                } else if (std::find(diverge_positions.begin(), diverge_positions.end(), pos) != diverge_positions.end()) {
                    std::cout << diverge_char; // Mark diverge point
                } else {
                    std::cout << lane_char; // Standard lane segment
                }
            } else {
                std::cout << " "; // Empty space for lanes that don't exist
            }
        }
        std::cout << " |\n"; // Right border for lane
    }
    std::cout.flush();
}
