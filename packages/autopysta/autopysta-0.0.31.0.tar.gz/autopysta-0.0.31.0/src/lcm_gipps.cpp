#include "lcm_gipps.h"

p_lcm_gipps::p_lcm_gipps() : p_lcm_gipps(0.9, 0.95)
{
}

p_lcm_gipps::p_lcm_gipps(double pvlow, double pvhigh)
{
	if (!(0 < pvlow && pvlow < pvhigh && pvhigh < 1)) {
		throw Exception(901, "Wrong parameters. Check 0 < pvlow < pvhigh < 1");
	}
	_pvl = pvlow;
	_pvh = pvhigh;
}

bool lcm_gipps::is_lch_possible(Point* /* leader */, Point * subject, Point * new_leader, Point * new_follower, Model *m, params* /* plc */)
{
	//puede cambiar: no choca con lider
	//               dist. de seguridad al lider
	//               no choca con follower
	//               dist. de seguridad al follower
	double sn = m->equil_spcg(0, 0);
	if ((new_leader == nullptr || (subject->X() + sn < new_leader->X() &&
		new_leader->X() - sn >= subject->X() + m->equil_spcg(new_leader->V(), subject->V()))) &&
		(new_follower == nullptr || (new_follower->X() + sn < subject->X() &&
			subject->X() - sn >= new_follower->X() + m->equil_spcg(subject->V(), new_follower->V())))
		) return true;
	return false;
}

lcm_gipps::lcm_gipps()
{
	_lcpars = new p_lcm_gipps();
}

lcm_gipps::lcm_gipps(p_lcm_gipps * p)
{
	_lcpars = p;
}

bool lcm_gipps::lch_left(Point *leader, Point *subject, Point *new_leader, Point *new_follower, Model *cfm, params *lcmpars) {
	Model *m = PICK(cfm, _cf);

	p_lcm_gipps *plc = (p_lcm_gipps*)PICK(lcmpars, _lcpars);

	//conviene cambiar
	if (plc->_pvl*m->free_flow_speed() > subject->V())
		return is_lch_possible(leader, subject, new_leader, new_follower, m, plc);
	return false;
}

bool lcm_gipps::lch_right(Point *leader, Point *subject, Point *new_leader, Point *new_follower, Model *cfm, params *lcmpars) {
	Model *m = PICK(cfm,_cf);

	p_lcm_gipps *plc = (p_lcm_gipps*)PICK(lcmpars,_lcpars);

	//conviene cambiar
	if (plc->_pvh*m->free_flow_speed() < subject->V())
		return is_lch_possible(leader, subject, new_leader, new_follower, m, plc);
	return false;
}
