cmake_minimum_required (VERSION 3.5)

project(sim-beta)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Add sub directories
add_subdirectory(framework)
add_subdirectory(simulator)
#add_subdirectory(operation)
add_subdirectory(statevector)
