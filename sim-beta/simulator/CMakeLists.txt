project(simulator)

# Create the executable
add_executable(${PROJECT_NAME} main.cpp)

if (GFLAGS_USE_TARGET_NAMESPACE)
    if (TARGET gflags::gflags)
        target_link_libraries(${PROJECT_NAME}
            # sub::op 
            sub::state 
            sub::frame
            gflags::gflags
        )
    else ()
        message(FATAL_ERROR "gflags::gflags target not defined")
    endif()
endif()
