#include "params/params.h"
#include "params/p_linear.h"
#include "params/p_idm.h"
#include "params/p_gipps.h"

#include "models/model.h"
#include "models/gipps.h"
#include "models/idm.h"
#include "models/linear.h"
#include "models/newell.h"

#include "creators/creator.h"
#include "creators/fixed_state_creator.h"
#include "creators/fixed_demand_creator.h"

#include "point.h"
#include "vehicle.h"
#include "lcm_gipps.h"
#include "geometry.h"
#include "simulation.h"
#include "trajectory.h"
#include "no_lch.h"

#include <iostream>
#include <vector>

using namespace std;

int main()
{
	p_gipps *pc = new p_gipps(1, -1, 6.5, 10, 0.8, -1);
	gipps *mc = new gipps(pc);
	p_gipps *pa = new p_gipps(1.7, -3.4, 6.5, 120.0/3.6, 0.8, -3.2);
	gipps *ma = new gipps(pa);
	//gipps *mi = new gipps();
	idm *mi = new idm();
	
	//Vectores para trayectorias conocidas
	vector<Point*> know_trajectory = vector<Point*>();
	vector<Point*> know_trajectory2 = vector<Point*>();
	
	for(int i = 0; i<1000; i++){
		Point * p1 = new Point(i/10.0, i - 100*cos(i/100.), 10+10*sin(i/10.), 0.1, 3);
		Point * p2 = new Point(i/10.0, 100 + i - 100*cos(i/100.), 10+10*sin(i/10.), 0.1, 1);
		know_trajectory.push_back(p1);
		know_trajectory2.push_back(p2);
	}
	
	Vehicle * v_kt1 = new Vehicle(know_trajectory);
	Vehicle * v_kt2 = new Vehicle(know_trajectory2);
	

	Vehicle * v1 = new Vehicle(ma, 400, 10, 1);
	Vehicle * v2 = new Vehicle(mi, 40, 5, 1);
	Vehicle * v3 = new Vehicle(ma, 300, 0, 1);
	
	vector<Vehicle*> vv = vector<Vehicle*>();
	vv.push_back(v1);
	vv.push_back(v_kt1);
	vv.push_back(v_kt2);
	vv.push_back(v2);
	vv.push_back(v3);
	

	Geometry *geometria_nueva = new Geometry(1000, 3, 300, 700);

	Creator *c1 = new FixedStateCreator(mi, 20, 10);
	Creator *c2 = new FixedStateCreator(mi, 20, 10);
	Creator *c3 = new FixedStateCreator(mc, 20, 10);
	vector<Creator*> ccrr = vector<Creator*>();
	ccrr.push_back(c1);
	ccrr.push_back(c2);
	ccrr.push_back(c3);
	
	//no_lch *glch = new no_lch();
	lcm_gipps *glch = new lcm_gipps();
	/*
	cout << mi->equil_spcg(120.0 / 3.6, 120.0 / 3.6) << endl;
	cout << version() << endl;
	cout << "mc " << mc << endl;
	cout << "ma " << ma << endl;
	cout << "mi " << mi << endl;
	*/
	Simulation nueva_simulacion = Simulation(glch, 15, geometria_nueva, ccrr, vv, 0.1);
	//cout << "sobrevivi al constructor" << endl;
	nueva_simulacion.run();

    return 0;
}
