cmake_minimum_required(VERSION 3.15...3.29)
project(
  ${SKBUILD_PROJECT_NAME}
  DESCRIPTION "A Python Package for Analyzing Lattice Polytopes"
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES C CXX)

set(POLY_Dmax
    11
    CACHE STRING "Maximum polytope dimension")

add_subdirectory(extern/palp)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(pypalp src/pypalp/pypalp.cpp)
target_link_libraries(pypalp PRIVATE objects class_objects nef_objects
                                     mori_objects)
target_compile_definitions(pypalp PRIVATE POLY_Dmax=${POLY_Dmax})
target_include_directories(pypalp PRIVATE ${CMAKE_SOURCE_DIR}/extern/palp
                                          ${CMAKE_SOURCE_DIR}/include)
target_compile_features(pypalp PRIVATE cxx_std_17)

install(TARGETS pypalp DESTINATION .)
