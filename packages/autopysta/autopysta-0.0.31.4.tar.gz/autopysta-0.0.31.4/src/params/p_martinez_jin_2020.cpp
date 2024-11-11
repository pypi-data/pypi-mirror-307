#include "params/p_martinez_jin_2020.h"

p_martinez_jin_2020::p_martinez_jin_2020() : p_newell(30.0, 0.0, 0.0) {}

p_martinez_jin_2020::p_martinez_jin_2020(double u, double tau) : p_newell(u, 0.0, 0.0)
{
    this->tau = tau;
    this->u = u;
}
