cmake_minimum_required(VERSION 3.12)
project(autopysta LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# CMake policies to handle SWIG and Python modules properly
cmake_policy(SET CMP0078 NEW)  # SWIG generates standard target names
cmake_policy(SET CMP0086 NEW)  # SWIG honors SWIG_MODULE_NAME via -module flag
cmake_policy(SET CMP0148 NEW)  # Use modern Python find modules

# Find the required packages: SWIG and Python3
find_package(SWIG REQUIRED)
include(UseSWIG)

# Display SWIG and Python3 information (for debugging purposes)
if(SWIG_FOUND)
    message(STATUS "SWIG found: ${SWIG_EXECUTABLE} (version: ${SWIG_VERSION})")
endif()

message(STATUS "Python3 found:")
message(STATUS "  Executable    : ${Python3_EXECUTABLE}")
message(STATUS "  Version       : ${Python3_VERSION}")
message(STATUS "  Include dirs  : ${Python3_INCLUDE_DIRS}")
message(STATUS "  Library       : ${Python3_LIBRARIES}")


# Define the SWIG interface file and the C++ source files
set(SWIG_INTERFACE ${CMAKE_SOURCE_DIR}/swig/autopysta.i)
file(GLOB_RECURSE AUTOPYSTA_SRC "${CMAKE_SOURCE_DIR}/src/*.cpp")

# Add include directories (Python and project-specific headers)
include_directories(${Python3_INCLUDE_DIRS} ${CMAKE_SOURCE_DIR}/include)

set_source_files_properties(${SWIG_INTERFACE} PROPERTIES CPLUSPLUS ON)

# Generate SWIG bindings for Python (autopysta module)
swig_add_library(autopysta
    LANGUAGE python
    SOURCES ${SWIG_INTERFACE} ${AUTOPYSTA_SRC}
)

set(SWIG_FLAGS "-Wall" "-doxygen")


# Set SWIG to explicitly use C++ mode with additional flags
set_property(SOURCE ${SWIG_INTERFACE} PROPERTY SWIG_FLAGS "-c++")

target_link_libraries(autopysta ${Python3_LIBRARIES})

# Compiler-specific options (GCC/Clang/MSVC)
if (MSVC)
    target_compile_options(autopysta PRIVATE 
        /W3 /EHsc /WX- 
        /D_CRT_SECURE_NO_WARNINGS
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # Use compatible flags for GCC and Clang
    target_compile_options(autopysta PRIVATE 
        -Wall -Wundef -Wpedantic -Wextra 
        -Wuninitialized -Winit-self 
        -Wno-missing-field-initializers
        -Wno-unknown-pragmas
    )
endif()

if (WIN32)
    message(STATUS "Building on Windows")
elseif(APPLE)
    message(STATUS "Building on macOS")
else()
    message(STATUS "Building on Linux")
endif()

# Add SWIG specific compile options (for additional SWIG flags)
set_property(TARGET autopysta PROPERTY SWIG_COMPILE_OPTIONS ${SWIG_FLAGS})

message(STATUS "Project configuration complete.")
