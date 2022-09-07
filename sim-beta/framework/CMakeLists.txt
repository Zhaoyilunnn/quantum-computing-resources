project (framework)

add_library(${PROJECT_NAME} 
    src/circuit.cpp 
    src/operation.cpp
)
add_library(sub::frame ALIAS ${PROJECT_NAME})

target_include_directories(${PROJECT_NAME}
    PUBLIC ${PROJECT_SOURCE_DIR}/include    
)
