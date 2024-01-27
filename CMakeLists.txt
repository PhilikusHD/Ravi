# CMakeLists.txt for Ravi project
cmake_minimum_required(VERSION 3.20)

# Specify the compiler (clang++)
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

project(Ravi)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Set the generator to Ninja
set(CMAKE_GENERATOR Ninja)

# Set the output directories for different configurations
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib-${CMAKE_BUILD_TYPE})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib-${CMAKE_BUILD_TYPE})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin-${CMAKE_BUILD_TYPE})

# Add the source files in Ravi/src directory
file(GLOB_RECURSE SOURCES Ravi/src/*.c)



# Add the pocketsphinx library
find_library(POCKETSPHINX_LIBRARY pocketsphinx)
if(NOT POCKETSPHINX_LIBRARY)
message(FATAL_ERROR "pocketsphinx library not found.")
endif()

# Try to find portaudio and pulseaudio with pkg-config
find_package(PkgConfig QUIET)

# Include directories
include_directories(Ravi/src/*.h ${PULSEAUDIO_INCLUDE_DIRS})
# Create the executable
add_executable(Ravi ${SOURCES})

# Link the pocketsphinx library
target_link_libraries(Ravi ${POCKETSPHINX_LIBRARY} ${PULSEAUDIO_LIBRARIES} m)