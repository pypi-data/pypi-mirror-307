#ifndef EXCEPTION_H
#define EXCEPTION_H

#include <exception>
#include <string>
#include <vector>

/**
 * @class Exception
 * @brief A custom exception class for handling errors in the Autopysta application.
 *
 * This class provides detailed error handling with error codes and messages, facilitating
 * better debugging and error tracking within the application. It is exposed to Python, allowing
 * Python code to catch and handle C++ exceptions from Autopysta.
 */
class Exception : public std::exception {
public:
    /**
     * @brief Constructs an Exception with a specific error code and message.
     * @param code Error code representing the type of error.
     * @param message Detailed error message providing context for the exception.
     */
    Exception(int code, const std::string& message);

    /**
     * @brief Retrieves the error code associated with the exception.
     * @return An integer representing the error code.
     */
    int code() const noexcept;

    /**
     * @brief Retrieves the detailed error message.
     * @return A const reference to a string containing the error message.
     */
    const std::string& message() const noexcept;

    /**
     * @brief Provides a description of the exception, including the error code and message.
     * @return A C-style string with a combined error code and message, safe for logging.
     */
    const char* what() const noexcept override;

    ~Exception() noexcept override = default;

private:
    int error_code_;              //!< Error code identifying the type of exception.
    std::string error_message_;   //!< Detailed error message.
    mutable std::string what_buffer_; //!< Buffer to store formatted message for what().
};

#endif // EXCEPTION_H
