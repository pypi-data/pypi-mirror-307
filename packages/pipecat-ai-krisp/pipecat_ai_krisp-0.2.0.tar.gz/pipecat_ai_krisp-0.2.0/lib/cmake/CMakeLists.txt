cmake_minimum_required(VERSION 3.5)

if (WIN32)
    include(visualstudio.cmake NO_POLICY_SCOPE)
endif()

project(pipecat-ai-krisp)

# Set 'Release' or 'Debug'
set(CMAKE_BUILD_TYPE Debug)

get_filename_component(ROOT_DIR ${PROJECT_SOURCE_DIR} DIRECTORY)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${ROOT_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${ROOT_DIR}/bin)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(UNIX OR APPLE)
    add_compile_options(-Wall -pedantic -Wno-undefined-func-template)

    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
        add_compile_options(-Wextra -Wconversion -Wsign-conversion
                -Wno-deprecated-declarations)
    endif()

    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        add_compile_options(
                -Weverything
                -Wno-c++98-compat-pedantic
                -Wno-documentation-pedantic
                -Wdeprecated-declarations
                -Wno-deprecated-declarations
                -Wno-padded
        )
    endif()
endif()

message("KRISP_SDK_PATH: ${KRISP_SDK_PATH}")
if (NOT DEFINED KRISP_SDK_PATH)
    message(FATAL_ERROR "KRISP_SDK_PATH must be specified")
endif()

set(KRISP_INC_DIR ${KRISP_SDK_PATH}/include)

# Krisp SDK libraries are applied to all targets
include(krisp.cmake)

if (WIN32)
    add_compile_definitions(KRISP_AUDIO_STATIC)
endif()
if (WIN32 AND MSVC)
    add_compile_definitions(_ITERATOR_DEBUG_LEVEL=0)
endif()

# Building krisp for Python
find_package(Python3 COMPONENTS NumPy REQUIRED)
find_package(pybind11 REQUIRED)

set(PYMODNAME_NC krisp_python)
pybind11_add_module(
        ${PYMODNAME_NC}
        ../krisp_python_module.cpp
)
target_include_directories(
        ${PYMODNAME_NC}
        PRIVATE
        ${KRISP_INC_DIR}
)
target_link_libraries(
        ${PYMODNAME_NC}
        PRIVATE Python3::NumPy
        ${KRISP_LIBS}
)
