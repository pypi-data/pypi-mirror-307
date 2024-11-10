cmake_minimum_required(VERSION 3.15)
project(qumeas)


include(GNUInstallDirs)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_compile_options(-fPIC)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)

# Output directories
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python/qumeas)

# Directory for eigen & pybind11
set(EXTERNAL_DIR ${CMAKE_SOURCE_DIR}/external)
file(MAKE_DIRECTORY ${EXTERNAL_DIR})
message(STATUS "Created external directory for Eigen & pybind11 if not found")

function(clone_if_missing url dir)
    if(NOT EXISTS ${dir})
        message(STATUS "Cloning ${url} into ${dir}...")
        execute_process(COMMAND git clone --depth 1 ${url} ${dir})
    else()
        message(STATUS "${dir} exists. Skipping clone.")
    endif()
endfunction()

# Eigen
find_package(Eigen3 QUIET)
if(NOT TARGET Eigen3::Eigen)
    message(STATUS "Eigen3 not found. Clonning into /external.")
    set(EIGEN_DIR ${EXTERNAL_DIR}/eigen)
    clone_if_missing("https://gitlab.com/libeigen/eigen.git" ${EIGEN_DIR})
    include_directories(${EIGEN_DIR})
else()
    message(STATUS "Eigen found.")
endif()

# pybind11
find_package(pybind11 QUIET)
if(NOT TARGET pybind11::module)
    message(STATUS "pybind11 not found. Clonning into /external.")
    set(PYBIND11_DIR ${EXTERNAL_DIR}/pybind11)
    clone_if_missing("https://github.com/pybind/pybind11.git" ${PYBIND11_DIR})
    add_subdirectory(${PYBIND11_DIR})
else()
    message(STATUS "pybind11 found")
endif()


# Enable OpenMP
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    message(STATUS "Found OpenMP")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

# Add subdirectories
add_subdirectory(src/cpp)
add_subdirectory(src/bindings)

# Platform-Specific Adjustments
if (CMAKE_SYSTEM_NAME STREQUAL "Darwin")  # macOS
    message(STATUS "Configuring for macOS")
    set(CMAKE_MACOSX_RPATH ON)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".dylib")

elseif (CMAKE_SYSTEM_NAME STREQUAL "Linux")  # Linux
    message(STATUS "Configuring for Linux")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

elseif (CMAKE_SYSTEM_NAME STREQUAL "Windows")  # Windows
    message(STATUS "Configuring for Windows")
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".dll")
    
    if (MSVC)
        add_compile_options(/W4 /WX)  # Treat warnings as errors in MSVC
    endif()
endif()
