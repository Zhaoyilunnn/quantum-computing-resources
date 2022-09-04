# Set the project name
project (statevector)

# Add a library with the above sources
add_library(${PROJECT_NAME} src/statevector.cpp src/chunk.cpp)
add_library(sub::state ALIAS ${PROJECT_NAME})

target_include_directories( ${PROJECT_NAME}
    PUBLIC ${PROJECT_SOURCE_DIR}/include
)

target_link_libraries(${PROJECT_NAME}
    sub::frame 
)
