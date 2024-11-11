#include "random_generator.h"

std::mt19937_64 RandomGenerator::generator;

void RandomGenerator::init(unsigned long seed) 
{
    generator.seed(seed);
	//std::random_device rd;
	//generator{ rdev() };
}

double RandomGenerator::uniform01()
{
    return uniform(0.0, 1.0);
}

double RandomGenerator::uniform(double a, double b)
{
    std::uniform_real_distribution<double> distribution(a, b);
	return distribution(generator);
}

double RandomGenerator::logistic(double location, double scale)
{
    double u = uniform01();
    return location + scale * std::log(u / (1 - u));
}

double RandomGenerator::normal(double mean, double stddev)
{
    std::normal_distribution<double> distribution(mean, stddev);
    return distribution(generator);
}

