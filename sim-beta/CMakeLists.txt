cmake_minimum_required (VERSION 3.5)

project(sim-beta)

set(CMAKE_BUILD_TYPE Debug)
set(GFLAGS_USE_TARGET_NAMESPACE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Set up google test: https://google.github.io/googletest/quickstart-cmake.html
include(FetchContent)
FetchContent_Declare(
  googletest
  # Specify the commit you depend on and update it regularly.
  URL https://github.com/google/googletest/archive/refs/tags/release-1.12.1.zip
)

# For Windows: Prevent overriding the parent project's compiler/linker settings
FetchContent_MakeAvailable(googletest)

find_package(gflags REQUIRED)

# Add sub directories
add_subdirectory(framework)
add_subdirectory(simulator)
add_subdirectory(statevector)

# enable CTest testing
include(CTest)
enable_testing()
add_subdirectory(test)
