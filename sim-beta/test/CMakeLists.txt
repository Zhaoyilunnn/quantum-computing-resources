project (simtest)

# Unit test
add_executable(${PROJECT_NAME} src/chunk_test.cpp)

target_link_libraries(${PROJECT_NAME}
    gtest_main
    sub::state
)

#enable_testing()
add_test(NAME test_all COMMAND ${PROJECT_NAME})

