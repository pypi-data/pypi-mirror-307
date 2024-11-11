#include "models/newell.h"

newell::newell()
{
    p_newell* p = new p_newell();
    pars = p;
    initialize_parameters(p);
}

newell::newell(p_newell* p)
{
    pars = p;
    initialize_parameters(p);
}

void newell::initialize_parameters(p_newell* p)
{
    tau = static_cast<float>(1.0f / (p->kj * p->w));
    sj = 1.0f / p->kj;
}

double newell::accel(Point* leader, Point* follower, params* p)
{
    Point* pt = new_point(leader, follower, p);
    double a = pt->A();
    delete pt;
    return a;
}

double newell::equil_spcg(double vl, double /* vf */, params* p)
{
    p_newell* q = (p_newell*)PICK(p, pars);
    return (vl + q->w) / (q->w * q->kj);
}

double newell::wave_speed(Point* /* leader */, Point* /* follower */, params* p)
{
    p_newell* q = (p_newell*)PICK(p, pars);
    return q->w;
}

double newell::free_flow_speed(params* p)
{
    p_newell* q = (p_newell*)PICK(p, pars);
    return q->u;
}

Point* newell::new_point(Point* /* leader */, Point* /* follower */, params* /* p */)
{
    return nullptr;
}

Point* newell::new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p)
{
    p_newell* q = (p_newell*)PICK(p, pars);
    float tau_steps = -(tau / Clock::dt);
    Point* subject = follower->get_current_point();
    double nx = subject->X() + q->u * Clock::dt;
    double nv = q->u;
    double nt = subject->T() + Clock::dt;

    if (leader != nullptr) {
        Point* delayed_leader = (*leader)[tau_steps];
        double xc = delayed_leader->X() - sj;
        if (xc < subject->X()) xc = subject->X();
        if (xc < nx) {
            nv = delayed_leader->V();
            nx = xc;
        }
    }
    return new Point(
        nt,
        nx,
        nv,
        (nv - subject->V()) / Clock::dt,
        subject->LANE()
    );
}
