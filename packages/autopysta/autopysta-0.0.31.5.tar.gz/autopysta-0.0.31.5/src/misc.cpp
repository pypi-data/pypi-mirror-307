#include "misc.h"

#include <Python.h>
#include <sstream>
#include <string>
#include <iomanip>


std::string version() {
    std::stringstream ss;
    ss << "=============================" << std::endl;
    ss << "  Version Info" << std::endl;
    ss << "=============================" << std::endl;
    ss << "  Version:        " << AUTOPYSTA_VERSION << std::endl;
    ss << "  Build Date:     " << __DATE__ << " " << __TIME__ << std::endl;
    
    #if defined __linux__
        ss << "  Platform:       Linux" << std::endl;
    #elif defined _WIN32
        ss << "  Platform:       Windows" << std::endl;
    #elif defined __APPLE__
        ss << "  Platform:       macOS" << std::endl;
    #else
        ss << "  Platform:       Unknown\n";
    #endif

    ss << "  Python Version: " << PY_MAJOR_VERSION << "." << PY_MINOR_VERSION << std::endl;
    ss << "=============================" << std::endl;

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
