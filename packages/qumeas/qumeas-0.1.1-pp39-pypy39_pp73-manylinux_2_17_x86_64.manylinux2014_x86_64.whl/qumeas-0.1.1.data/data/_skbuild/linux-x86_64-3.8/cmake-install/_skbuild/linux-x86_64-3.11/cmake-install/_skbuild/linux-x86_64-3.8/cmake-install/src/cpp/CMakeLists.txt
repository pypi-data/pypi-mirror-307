set(SOURCES
    cumulant_expectation.cc
    expectation_basis.cc
    expectation_cumu_1b.cc
    expectation_cumu_2b.cc
    expectation_cumu_3b.cc
    expectation_cumu_4b.cc
    expectation_exact.cc
    partition.cc
    quantum_utils.cc
)

add_library(qumeas_core ${SOURCES})

if(OpenMP_CXX_FOUND)
    target_link_libraries(qumeas_core PUBLIC OpenMP::OpenMP_CXX)
endif()

target_include_directories(qumeas_core PUBLIC ${CMAKE_SOURCE_DIR}/include)
