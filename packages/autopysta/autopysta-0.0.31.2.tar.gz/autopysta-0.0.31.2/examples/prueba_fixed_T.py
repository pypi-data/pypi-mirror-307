#import sys
#sys.path.append('../autopysta/')
#import autopysta as ap

import autopysta as ap
import matplotlib.pyplot as plt
from numpy import cos, sin


# Display the current version of autopysta library
print(ap.version())

# Define velocity values for vehicles
vl = 120.0 / 3.6  # Target velocity in m/s
vlc = 10          # Cruise velocity

# Define vehicle parameters and models
pc = ap.p_gipps(1, -1, 6.5, vlc, 0.8, -1)  # Parameters for a vehicle model
mc = ap.gipps(pc)                          # Instantiate the Gipps model with parameters
pa = ap.p_gipps(1.7, -3.4, 6.5, vl, 0.8, -3.2)  # Alternate set of parameters for another model
ma = ap.gipps(pa)                          # Another Gipps model instance with different parameters
mi = ap.newell()                           # Instantiate the Newell model

# Create sample vehicle trajectories and lane data
known_trajectory = []
known_trajectory2 = []
lanes2 = []
for i in range(900):
    # Define trajectory points with position, speed, and lane
    known_trajectory.append(ap.Point(i / 10.0, i - 100 * cos(i / 100.0 + 2), 10 + 10 * sin(i / 10.0), 0.1, 1))
    known_trajectory2.append(100 + i - 100 * cos(i / 100.0))
    lanes2.append(int(((i / 200) % 3) + 1))

# Initialize vehicles with defined trajectories
try:
    my_car = ap.Vehicle(known_trajectory)
    my_car2 = ap.Vehicle(known_trajectory2, lanes2)
except ap.AutopystaException as exc:
    print(exc)


# Check if trajectories contain sufficient points for the simulation duration
if len(known_trajectory) < 900:
    print("Warning: known_trajectory has insufficient points for the simulation duration.")
if len(known_trajectory2) < 900:
    print("Warning: known_trajectory2 has insufficient points for the simulation duration.")

# Vehicle instances for simulation, some with specified models and parameters
vehicles = [
    ap.Vehicle(mc, 100, vlc, 1),
    my_car,
    my_car2,
    ap.Vehicle(mc, 100, vlc, 2),
    ap.Vehicle(mc, 40, 0, 1)
]

# Define highway geometry for the simulation
try:
    geo = ap.Geometry(1000, 3)
except ap.AutopystaException as e:
    print(e)
    
# Set up vehicle creators for each lane in the simulation
creators = [
    ap.FixedStateCreator(mi, 20, 10),
    ap.FixedStateCreator(mc, 20, 10),
    ap.FixedStateCreator(mi, 20, 10)
]

# Choose lane-changing model and create a simulation object
lane_change_model = ap.lcm_gipps()
sim = ap.Simulation(lane_change_model, 90, geo, creators, vehicles, 0.1)

# Run the simulation
try:
    results = sim.run()
except ap.AutopystaException as e:
    print(e)


# Plot vehicle trajectories across lanes
results.plot_x_vs_t()  # All lanes
results.plot_x_vs_t(1) # Lane 1
results.plot_x_vs_t(2) # Lane 2
results.plot_x_vs_t(3) # Lane 3

# Calculate Edie's flow and density in specified time-space regions
edie_data = results.edie(24, 32, 2, 100, 150, 2)
for index, values in enumerate(edie_data):
    print("Box {:3d}: Q: {:5.3f}, K: {:5.3f}".format(index, values[0], values[1]))

# Retrieve and plot vehicle positions at a specific time and distance
time = 43.113605
points_at_time = results.passes_on_t(time, 2)
dist = 200.5
times_to_cross_dist = results.passes_on_x(dist, 2)

trys = results.by_lane(2)

plt.figure()
tt = [trys[0][i].T() for i in range(len(trys[0]))]
xx = [trys[0][i].X() for i in range(len(trys[0]))]

plt.plot(tt, xx, 'b-')
for pi in range(1, len(trys)):
    pd = trys[pi]
    p=pd[0].LANE()
    tt=[pd[i].T() for i in range(len(pd))]
    xx=[pd[i].X() for i in range(len(pd))]
    plt.plot(tt,xx,'b-')

time_pass_t = [points_at_time[i].T() for i in range(len(points_at_time))]
time_pass_x = [points_at_time[i].X() for i in range(len(points_at_time))]
distance_pass_t = [times_to_cross_dist[i].T() for i in range(len(times_to_cross_dist))]
distance_pass_x = [times_to_cross_dist[i].X() for i in range(len(times_to_cross_dist))]

plt.plot(time_pass_t, time_pass_x, 'ro')
plt.plot([time, time], [0, 750], 'r')
plt.plot(distance_pass_t, distance_pass_x, 'go')
plt.plot([0, 90], [dist, dist], 'g')

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Trajectories in Lane 2 with Points of Interest")
plt.show()
