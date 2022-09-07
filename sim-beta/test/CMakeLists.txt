project (simtest)

# Unit test
add_executable(${PROJECT_NAME} 
    src/chunk_test.cpp
    src/circuit_test.cpp
)

target_link_libraries(${PROJECT_NAME}
    gtest_main
    sub::state
)

target_include_directories(${PROJECT_NAME}
    PUBLIC ${PROJECT_SOURCE_DIR}/include    
)

#enable_testing()
#add_custom_target(test_circ COMMAND touch data/cluster.json)
#add_dependencies(${PROJECT_NAME} test_circ)
add_test(NAME test_all COMMAND ${PROJECT_NAME} WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

