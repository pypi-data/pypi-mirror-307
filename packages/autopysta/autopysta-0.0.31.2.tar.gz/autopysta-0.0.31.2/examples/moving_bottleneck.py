# ------------------------------------------------------------------------------
# Case of study: Moving Bottleneck
#
# In this example we define 2 lanes, with no on/off ramps. On the second lane 
# there will be a slow vehicle (simulating a truck) that will go with a constant 
# velocity of 5 m/s (18 km/h) and the creators of both lanes will create 5 vehicles 
# each with an bigger initial speed than the truck, forcing the vehicles on the 
# second lane to change to the first lane.
# ------------------------------------------------------------------------------

# Import the library
import autopysta as ap

# We define the model the truck will follow and the parameters it will use, in this case we input a slow velocity 
# to generate a bottleneck.
V = 20 / 3.6
c1 = 1.0 / 20.0
c2 = 93.0 / 160.0
c3 = 9.0 / 64.0
sr = 220.0 / 9
tau = 4.0 / 6
p_li = ap.p_linear(V, c1, c2, c3, sr, tau)
li = ap.linear(p_li)

# A vehicle with the given model is created, along with its x position and initial 
# speed. Something to note is that if any exception would occur, it would be catched 
# as an exception class defined in the library (AutopystaException).
try:
    my_car = ap.Vehicle(li, 0, V, 2)
except ap.AutopystaException as exc:
    print (exc)

# A list of vehicles with given trajectories is created, in this case only 
# containing the truck.
vv=[my_car]

# Now we define the geometry of the highway the Simulation will use. It 
# takes as arguments the length of the highway, number of lanes, position where
# the merge ramp ends (0 for no merge ramp) and the position where the diverge
# ramp ends (length of the highway for no diverge ramp).
geo = ap.Geometry(1000, 2, 0, 1000)

# Define the acceleration/desacceleration model with default parameters the creators 
# are going to use. In this case IDM is going to be used for all the lanes.
idm = ap.idm()

# Next we define the types of creators each lane will use. The creators basically
# create vehicles when the necessary conditions (defined by each type of creator)
# are met. If only one is specified then all lanes will have that creator. The final 
# parameter is optional, it sets the number of vehicles to create (infinite by default).
ccrr=[
    ap.FixedStateCreator(idm, 15, 10, 20),
    ap.FixedStateCreator(idm, 15, 10, 20),
]

# One last setting to define is the lane-changing model. If the user don't want to
# allow lane changing then it can use the no_lch model.
lcm = ap.lcm_gipps()

# The Simulation object is defined the previous settings to run for 80 seconds and
# with a deltaTime of 0.1 seconds
s = ap.Simulation(lcm, 160, geo, ccrr, vv, 0.1)

# Finally, the Simulation is run, where upon finishing it will will return a results
# object, that contains important data about the trajectories from the Simulation.
r = s.run()

# The plot_x_vs_t method can be called to plot the trajectories of all lanes and 
# certain lanes
r.plot_x_vs_t()     # Plot all lanes
r.plot_x_vs_t(1)    # Plot lane 1
r.plot_x_vs_t(2)    # Plot lane 2
