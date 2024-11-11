/**
 * @file params.h
 * @author Rafael Delpiano.
 * @date 11 dec 2019
 * @brief File for the params and params_cust classes definitions (short description).
 *
 * @details A larger description about this file.
 * This is still part of the longer description.
 *
 * Another line.
 */

#ifndef _PARAMS
#define _PARAMS

#include <unordered_map>
#include <string>

/**
 * @brief Base class for car-following model parameters.
 *
 * This class is a base class that stores common or general parameters used by various car-following models.
 * Specific models, such as `newell`, will have their own parameter sets that inherit from this class.
 */
class params {
public:
    //! Default constructor for the params class.
    /*!
     * Initializes the base class for car-following model parameters.
     */
    params();
};

/**
 * @brief Custom parameters class for storing key-value pairs.
 *
 * This class inherits from the `params` class and stores custom parameters in a dictionary-like structure.
 * The `params_cust` class allows for flexible key-value pair storage of parameters.
 */
class params_cust : public params {
public:
     std::unordered_map<std::string, double> map; //!< Dictionary storing custom parameters.

    /*!
     * Initializes the dictionary for custom parameters.
     */
    params_cust();

    //! Adds a new parameter to the dictionary.
    /*!
     * @brief Adds a new parameter to the dictionary.
     *
     * @param new_name Key or name of the parameter.
     * @param new_value Value associated with the parameter.
     */
    void add(const std::string& new_name, double new_value);

    /*!
     * @brief  Retrieves the value of a parameter by its key.
     *
     * @param name Key or name of the parameter to retrieve.
     * @return The value associated with the given key.
     */
    double get(const std::string& name) const;
};

#endif
