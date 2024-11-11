# ------------------------------------------------------------------------------
# Case Study: Using Different Vehicle Creators
#
# This example demonstrates the use of different vehicle creators to populate 
# lanes with vehicles using distinct driving models. The creators used are:
# 1. `FixedStateCreator`: Generates vehicles with specified spacing and speed.
# 2. `FixedDemandCreator`: Generates vehicles based on a fixed traffic flow rate.
# ------------------------------------------------------------------------------

# Import the library
import autopysta as ap

# Display the current version of autopysta
print(ap.version())

# Define the highway geometry for the simulation. The Geometry object takes:
# 1. `length`: The length of the highway (meters).
# 2. `lanes`: Number of lanes.
# 3. `merge_pos`: Position where a merge ramp ends (0 for no merge ramp).
# 4. `diverge_pos`: Position where a diverge ramp starts (highway length for no diverge ramp).
length = 1000
initial_lanes = 4
merge_position = 300
diverge_position = 700
highway_geometry = ap.Geometry(length, initial_lanes, merge_position, diverge_position)

# Define the driving models for acceleration/deceleration.
# Default parameters are used for both models.
idm_model = ap.idm()
gipps_model = ap.gipps()

# Specify the types of vehicle creators for each lane. The creators define the
# conditions under which vehicles are added to the lanes:
# - `FixedStateCreator`: Generates vehicles based on specified spacing and speed.
# - `FixedDemandCreator`: Generates vehicles based on a fixed flow rate.
# If only one creator is given, it will apply to all lanes. The final parameter 
# is optional, specifying a maximum number of vehicles (default is unlimited).
spacing = 15
speed = 10
flow_rate = 0.5
lane_creators = [
    ap.FixedStateCreator(gipps_model, spacing, speed),  # Lane 1
    ap.FixedDemandCreator(idm_model, flow_rate),        # Lane 2
    ap.FixedStateCreator(idm_model, spacing, speed),    # Lane 3
    ap.FixedDemandCreator(gipps_model, flow_rate),      # Lane 4 (if present)
]


# Define the lane-changing model. To disable lane changing, use `no_lch`.
lane_change_model = ap.lcm_gipps()

# Initialize the Simulation object with the defined settings. The simulation is
# set to run for 80 seconds with a timestep of 0.1 seconds.
# No vehicles are predefined, so we use an empty list.
# We set verbose mode to get some extra output and see the shape of the geometry
total_time = 80
vehicles=[]
time_step = 0.1
verbose = True
simulation = ap.Simulation(
    lane_change_model,
    total_time,
    highway_geometry,
    lane_creators,
    vehicles,
    time_step
)


# Run the simulation. The `run()` method returns a `Results` object containing
# trajectory data from the simulation.
simulation_results = simulation.run()

# The `plot_x_vs_t` method generates trajectory plots. It can be used to plot
# all lanes or specific lanes, as shown below.
plotting = True
if (plotting):
    simulation_results.plot_x_vs_t()       # Plot all lanes
    simulation_results.plot_x_vs_t(lane=1) # Plot only lane 1
    simulation_results.plot_x_vs_t(lane=2) # Plot only lane 2
    simulation_results.plot_x_vs_t(lane=3) # Plot only lane 3
    simulation_results.plot_x_vs_t(lane=4) # Plot only lane 4 (if applicable)

