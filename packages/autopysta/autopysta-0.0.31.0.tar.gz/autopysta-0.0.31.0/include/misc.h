/**
 * @file misc.h
 * @author
 * @date 11 Dec 2019
 * @brief Header file containing miscellaneous utility functions and classes.
 *
 * @details This file contains the definition of various utility functions and classes
 * that serve as helpers for common operations such as version information, range checking,
 * and vector length validation. The functionality provided in this file is meant to
 * supplement other parts of the system with general-purpose utilities.
 */

#ifndef _MISC_AUTOPYSTA
#define _MISC_AUTOPYSTA

#include <string>
#include <sstream>
#include <ctime>
#include <vector>

/**
 * @brief Get the software version information.
 *
 * This function returns a string that contains the current version of the software, along
 * with the build date, time, and the system platform (Linux or Windows). It also includes
 * the version of Python being used in the environment.
 *
 * @return A string containing version, build date, system platform, and Python version.
 */
std::string version();

/**
 * @class test
 * @brief A utility class that provides common testing functions.
 *
 * This class contains utility functions for common tasks like checking if a number falls
 * within a range and checking the length of a vector. It is designed to be a lightweight
 * helper for various validation tasks.
 */
class test {
public:
    /**
     * @brief Check if a number is within an inclusive range.
     *
     * This method checks whether a given number lies between a minimum and a maximum value
     * (both bounds inclusive).
     *
     * @param number The number to be checked.
     * @param min The minimum allowable value.
     * @param max The maximum allowable value.
     * @return True if the number lies within the range, false otherwise.
     */
    static bool range_inc(double number, double min, double max);

    /**
     * @brief Check if a vector has a specific length.
     *
     * This method checks whether the size of the given vector matches the specified length.
     * It is a templated function, allowing it to work with vectors containing any data type.
     *
     * @tparam T The type of the elements in the vector.
     * @tparam A The allocator type for the vector (typically `std::allocator`).
     * @param v The vector to be checked.
     * @param l The required length of the vector.
     * @return True if the vector size matches the specified length, false otherwise.
     */
    template<typename T, typename A>
    static bool length(const std::vector<T, A>& v, int l);
};

#endif // _MISC_AUTOPYSTA
