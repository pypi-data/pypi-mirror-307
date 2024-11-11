#include "models/martinez_jin_2020.h"

martinez_jin_2020::martinez_jin_2020()
{
	p_martinez_jin_2020* p = new p_martinez_jin_2020();
	pars = p;
	initialize_parameters(p);
}

martinez_jin_2020::martinez_jin_2020(p_martinez_jin_2020* p)
{
	pars = p;
	initialize_parameters(p);
}

void martinez_jin_2020::initialize_parameters(p_martinez_jin_2020* p)
{
	tau = p->tau;
	sj = 1.0f / p->kj;
}
