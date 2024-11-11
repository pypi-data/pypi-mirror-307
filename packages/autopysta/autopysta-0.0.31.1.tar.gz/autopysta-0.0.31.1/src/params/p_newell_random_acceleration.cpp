#include "params/p_newell_random_acceleration.h"

p_newell_random_acceleration::p_newell_random_acceleration() : p_newell(60.0 / 3.6, 20.0 / 3.6, 0.15) {}

p_newell_random_acceleration::p_newell_random_acceleration(double u, double w, double kj, double sigma_tilde, double beta) : p_newell(u, w, kj) {
	this->sigma_tilde = sigma_tilde;
	this->beta = beta;
}
