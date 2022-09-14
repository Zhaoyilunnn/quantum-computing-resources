# Set the project name
project (statevector)

# Add a library with the above sources
add_library(${PROJECT_NAME} 
    src/statevector.cpp 
    src/chunk.cpp 
    src/util.cpp
)
add_library(sub::state ALIAS ${PROJECT_NAME})

target_include_directories( ${PROJECT_NAME}
    PUBLIC ${PROJECT_SOURCE_DIR}/include
)

find_package(Threads REQUIRED)
find_package(OpenMP REQUIRED)

target_link_libraries(${PROJECT_NAME}
    sub::frame 
    OpenMP::OpenMP_CXX 
    Threads::Threads
)

#find_package(Threads)
#target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})
#
#find_package(OpenMP)
#if(OpenMP_CXX_FOUND)
#    target_link_libraries(${PROJECT_NAME} PUBLIC OpenMP::OpenMP_CXX)
#endif()

