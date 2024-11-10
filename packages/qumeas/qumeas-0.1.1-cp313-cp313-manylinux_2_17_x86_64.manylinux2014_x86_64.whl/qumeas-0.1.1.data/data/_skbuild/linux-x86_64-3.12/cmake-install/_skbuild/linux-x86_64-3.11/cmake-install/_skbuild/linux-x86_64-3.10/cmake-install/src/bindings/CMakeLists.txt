pybind11_add_module(libmeas bindings.cc)

target_link_libraries(libmeas PRIVATE qumeas_core)

set_target_properties(libmeas PROPERTIES
    OUTPUT_NAME "libmeas"
)

install(TARGETS libmeas
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}
)
