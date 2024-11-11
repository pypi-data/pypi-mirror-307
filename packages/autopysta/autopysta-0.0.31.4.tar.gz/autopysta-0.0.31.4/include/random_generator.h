/**
 * @file random_generator.h
 * @author Rafael Delpiano.
 * @date 08 May 2022
 * @brief Provides utilities for generating random numbers using various probability distributions.
 *
 * @details This file defines the `RandomGenerator` class, providing a flexible API for generating 
 *          random numbers using common probability distributions (uniform, normal, and logistic). 
 *          The class includes an optional seed control for reproducibility.
 */

#ifndef _RANDOM_GENERATOR
#define _RANDOM_GENERATOR

#include <random>
#include <cmath>
#include <ctime>

/**
 * @brief Utility class for generating random numbers using various distributions.
 *
 * `RandomGenerator` provides static methods for generating random values from:
 * - Uniform distributions ([0,1] or [a,b])
 * - Normal (Gaussian) distribution
 * - Logistic distribution
 * 
 * The class uses a Mersenne Twister engine to produce high-quality random numbers.
 */
class RandomGenerator {
    static std::mt19937_64 generator; //!< Mersenne Twister 64-bit random number generator.

public:
    /**
     * @brief Initialize the random number generator with a seed.
     *
     * This method initializes the Mersenne Twister generator using the current time as the seed.
     * This ensures that the generator produces different random sequences each time the program runs.
     * @param seed Optional seed for the random generator. Uses current time if not provided.
     */
    static void init(unsigned long seed = static_cast<unsigned long>(std::time(nullptr)));

    /**
     * @brief Generate a random value from a uniform distribution [a, b].
     *
     * This method returns a random value sampled from a uniform distribution with bounds `a` and `b`.
     * 
     * @param a The minimum value of the distribution.
     * @param b The maximum value of the distribution.
     * @return A random double value between `a` and `b`.
     */
    static double uniform(double a = 0.0, double b = 1.0);

    /**
     * @brief Generate a random value from a standard uniform distribution [0, 1].
     *
     * This method returns a random value sampled from a uniform distribution between 0 and 1.
     *
     * @return A random double value between 0 and 1.
     */
    static double uniform01();

    /**
     * @brief Generate a random value from a logistic distribution.
     *
     * This method returns a random value sampled from a logistic distribution with location `mu` and scale `s`.
     * The logistic distribution is commonly used in various models, including machine learning and statistics.
     *
     * @param mu The location parameter of the logistic distribution (mean).
     * @param s The scale parameter (related to the standard deviation).
     * @return A random double value sampled from a logistic distribution.
     */
    static double logistic(double location = 0.0, double scale = 1.0);

    /**
     * @brief Generates a random value from a normal (Gaussian) distribution.
     *
     * @param mean The mean of the normal distribution.
     * @param stddev The standard deviation of the normal distribution.
     * @return A random double from the specified normal distribution.
     */
    static double normal(double mean = 0.0, double stddev = 1.0);

};

#endif // _RANDOM_GENERATOR
