import autopysta as ap
import matplotlib.pyplot as pt

print(ap.version())
vl = 120.0/3.6
vlc = 10

pc = ap.p_gipps(1, -1, 6.5, vlc, 0.8, -1)
mc = ap.gipps(pc)
pa = ap.p_gipps(1.7, -3.4, 6.5, vl, 0.8, -3.2)
ma = ap.gipps(pa)
pi = ap.p_idm(120.0,1.5,0.3,3.0,2.0,1.0)
mi = ap.linear()

vv = [ap.vehicle(ma, 100, vlc, 1),
      ap.vehicle(mc, 100, vlc, 2),
      ap.vehicle(ma, 40, 0, 1)]
# vv=[]

geo = ap.Geometry(1000, 2, 300, 700)
ccrr = [ap.FixedDemandCreator(mi, 0.5, 10), # 20, 0, 10),
        ap.FixedDemandCreator(mc, 0.45), # 20, 0),
        ap.FixedDemandCreator(mc, 0.42)] # 20, 0)]

lcm = ap.no_lch()
#lcm = ap.lcm_gipps()

s = ap.Simulation(lcm, 90, geo, ccrr, vv, 0.1)
r = s.run()
rlts = ap.Results
r.plot_x_vs_t()     #plot all lane
r.plot_x_vs_t(1)    #plot certain lane
r.plot_x_vs_t(2)
r.plot_x_vs_t(3)

d = r.edie(24, 32, 2, 600, 650, 1)
c = 0
for a in d:
    print("Box {:3d}: Q: {:5.3f}, K: {:5.3f}".format(c, a[0], a[1]))
    c+=1

time = 43.113605
points_at_time = r.passes_on_t(time, 2)

dist = 200.5
times_to_cross_dist = r.passes_on_x(dist, 2)

trys = r.by_lane(2)


pt.figure()
tt = [trys[0][i].T() for i in range(len(trys[0]))]
xx = [trys[0][i].X() for i in range(len(trys[0]))]

pt.plot(tt, xx, 'b-')
for pi in range(1, len(trys)):
    pd = trys[pi]
    p=pd[0].LANE()
    tt=[pd[i].T() for i in range(len(pd))]
    xx=[pd[i].X() for i in range(len(pd))]
    pt.plot(tt,xx,'b-')

time_pass_t = [points_at_time[i].T() for i in range(len(points_at_time))]
time_pass_x = [points_at_time[i].X() for i in range(len(points_at_time))]
distance_pass_t = [times_to_cross_dist[i].T() for i in range(len(times_to_cross_dist))]
distance_pass_x = [times_to_cross_dist[i].X() for i in range(len(times_to_cross_dist))]

pt.plot(time_pass_t, time_pass_x, 'ro')
pt.plot([time, time], [0, 750], 'r')
pt.plot(distance_pass_t, distance_pass_x, 'go')
pt.plot([0, 90], [dist, dist], 'g')

pt.show()
