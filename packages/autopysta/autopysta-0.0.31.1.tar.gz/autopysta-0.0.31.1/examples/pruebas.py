import autopysta as ap
import matplotlib.pyplot as pt

print(ap.version())
vl = 120.0/3.6
vlc = 10

pc = ap.p_gipps(1, -1, 6.5, vlc, 0.8, -1)
mc = ap.gipps(pc)
pa = ap.p_gipps(1.7, -3.4, 6.5, vl, 0.8, -3.2)
ma = ap.gipps(pa)
mi = ap.newell()

vv = [ap.vehicle(mc, 100, vlc, 1),
      ap.vehicle(mc, 100, vlc, 2),
      ap.vehicle(mc, 40, 0, 1)]
# vv=[]

geo = ap.Geometry(1000, 2, 300, 700)
ccrr = [ap.FixedDemandCreator(mi, 0.5, 10), # 20, 0, 10),
        ap.FixedDemandCreator(mi, 0.45), # 20, 0),
        ap.FixedDemandCreator(mc, 0.42)] # 20, 0)]

lcm = ap.no_lch()
# lcm = ap.lcm_gipps()

s = ap.Simulation(lcm, 90, geo, ccrr, vv, 0.1)
r = s.run()
rlts = ap.Results
pt.plot()

print(r)

# separa una trayectoria en los tramos recorridos en la misma pista
def porpista(tray):
    i = 0
    ult = tray[0].LANE()
    res = []
    act = []
    for i in range(len(tray)):
        pto = tray[i]
        if pto.LANE() != ult:
            res.append(act)
            ult = pto.LANE()
            act = [pto]
        else:
            act.append(pto)
        i += 1
    res.append(act)
    # print(i, totnd(res))
    return res


def graficar(trys):
    colores = ['g-', 'r-', 'b-', 'k-']
    pt.figure()
    tt=[trys[0][i].T() for i in range(len(trys[0]))]
    xx=[trys[0][i].X() for i in range(len(trys[0]))]
    pt.plot(tt,xx,colores[0])
    for auto in trys[1:]:
        pedazos=porpista(auto)
        for pd in pedazos:
            tt=[p.T() for p in pd]
            xx=[p.X() for p in pd]
            p=pd[0].LANE()
            pt.plot(tt,xx,colores[p])
    pt.show()

graficar(r)


