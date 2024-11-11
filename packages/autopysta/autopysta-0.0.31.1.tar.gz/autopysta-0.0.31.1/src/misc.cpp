#include "misc.h"

#include <Python.h>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>

std::string read_version() {
    std::ifstream version_file("VERSION");
    if (!version_file.is_open()) {
        return "Unknown Version";
    }
    std::stringstream ss;
    ss << version_file.rdbuf();
    return ss.str();
}

std::string version() {
    std::string version_str = read_version();
    std::stringstream ss;
    ss << "\n=============================\n";
    ss << "  Version Info\n";
    ss << "=============================\n";
    ss << "  Version:        " << version_str << "\n";
    ss << "  Build Date:     " << __DATE__ << " " << __TIME__ << "\n";
    
    #if defined __linux__
        ss << "  Platform:       Linux\n";
    #elif defined _WIN32
        ss << "  Platform:       Windows\n";
    #elif defined __APPLE__
        ss << "  Platform:       macOS\n";
    #else
        ss << "  Platform:       Unknown\n";
    #endif

    ss << "  Python Version: " << PY_MAJOR_VERSION << "." << PY_MINOR_VERSION << "\n";
    ss << "=============================\n";

    return ss.str();
}

bool test::range_inc(double number, double min, double max)
{
    return (number >= min && number <= max);
}

template<typename T, typename A>
bool test::length(const std::vector<T, A>& v, int l)
{
    return v.size() == l;
}
