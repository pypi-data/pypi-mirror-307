#include "models/newell_random_acceleration.h"
#include <iostream>

newell_random_acceleration::newell_random_acceleration() {
    auto* p = new p_newell_random_acceleration();
    pars = p;
    initialize_parameters(p);
}

newell_random_acceleration::newell_random_acceleration(p_newell_random_acceleration* p) {
    pars = p;
    initialize_parameters(p);
}

void newell_random_acceleration::initialize_parameters(p_newell_random_acceleration* p) {
    // Base parameters from Newell's model
    tau = static_cast<float>(1.0f / (p->kj * p->w));  // Reaction time, based on density and wave speed
    sj = 1.0 / p->kj;                                // Minimum spacing (jam density spacing)

    // Additional parameter for randomness: standard deviation of acceleration fluctuations
    double sigma = p->sigma_tilde * p->u * sqrt(p->beta);
    double ebt = exp(-p->beta * tau);                // Exponential decay factor for randomness

    // Standard deviation of ksi (random acceleration fluctuation), derived from Laval et al., 2014, Eq (5.b)
    ksi_std_dev = sqrt((pow(sigma, 2) / (2 * pow(p->beta, 3))) * (ebt * (4 - ebt) + 2 * p->beta * tau - 3));
}

void newell_random_acceleration::validate_parameters(params* p) {
	auto* q = (p_newell_random_acceleration*)PICK(p, pars);

    if (!q) throw Exception(902, "Invalid parameters for random acceleration model");

    // Ensure tau (1/(w*kj)) is an integer multiple of dt for discrete simulation steps
    double epsilon = 0.00001;
    if (abs((tau / Clock::dt) - static_cast<int>(tau / Clock::dt)) > epsilon) {
        throw Exception(901, "Error in parameters: 1/(w*kj) divided by dt must be an integer.");
    }

	//From (5.a) of Laval et al., 2014
    if (q->beta == 0) throw Exception(902, "Division by zero error in parameter beta.");
}

Point* newell_random_acceleration::new_point(GeneralizedTrajectory* leader, Trajectory* follower, params* p) {
	auto* q = (p_newell_random_acceleration*)PICK(p, pars);
	
    int tau_steps = static_cast<int>(-tau / Clock::dt);  // Delayed time steps based on tau
    Point* delayed_subj = (*follower)[tau_steps];        // Previous position of follower at delay time
    Point* subject = follower->get_current_point();      // Current position of the follower

    // Expected value for ksi (random speed increment) based on Laval's model, Eq (5.a)
    double v0 = subject->V();                            // Current speed of the follower
    double ksi_mean = q->u * Clock::dt - (1 - exp(-q->beta * Clock::dt)) * (q->u - v0) / q->beta;
    double ksi = RandomGenerator::normal(ksi_mean, ksi_std_dev); // Random acceleration term with variability

    // Update time, position, and velocity of the follower
    float nt = subject->T() + Clock::dt;                // Next time step
    float nx = subject->X() + ksi;                      // Position update with random fluctuation
    float nv = (nx - delayed_subj->X()) / tau;          // Velocity, based on new position and delay

    // Adjustments to prevent non-physical results
    if (nv < 0) {
        nx = follower->get_current_point()->X();
        nv = 0;
    }

    // Check for leader's influence (maintain safe following distance)
    if (leader != nullptr) {
        Point* delayed_leader = (*leader)[tau_steps];
        double xc = delayed_leader->X() - sj;           // Safe following distance

        // Ensure follower does not surpass leader
        if (xc < subject->X()) xc = subject->X();
        if (xc < nx) {
            nv = delayed_leader->V();
            nx = xc;
        }
    }
	
    // Compute acceleration as the change in velocity over the time step
    float na = (nv - subject->V()) / Clock::dt;

    return new Point(nt, nx, nv, na, subject->LANE());
}
