# Set the minimum required version of CMake
cmake_minimum_required(VERSION 3.27)

# Set Compiler
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

# Use the Ninja generator
set(CMAKE_GENERATOR Ninja)

# Set the C++ standard to C++20
set(CMAKE_CXX_STANDARD 20)

# Export compile commands for tooling
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set the output directories for different configurations
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib/${CMAKE_BUILD_TYPE})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib/${CMAKE_BUILD_TYPE})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/${CMAKE_BUILD_TYPE})

# Create the main executable for Ravi
project(Ravi)

file(GLOB_RECURSE SRC src/*.cpp)
add_executable(Ravi ${SRC})
target_include_directories(Ravi PRIVATE src)

include_directories(${CMAKE_SOURCE_DIR}/src/)

# Compiler-specific options for Debug build
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  add_compile_options(
    -g # Generate debug information
    -O0 # Disable optimizations
    -Wall # Enable all compiler warnings
    -Wextra # Enable extra compiler warnings
    -glldb # Enable debug info tuning for the lldb debugger
  )

  # Define a preprocessor macro for debug builds
  target_compile_definitions(Ravi PRIVATE RV_DEBUG)
  add_compile_definitions(Ravi PRIVATE RV_DEBUG)
  # Add runtime checks for debug builds
  target_compile_options(Ravi PRIVATE -fstack-protector)

  set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "-v")
endif()

# Compiler-specific options for Release build
if(CMAKE_BUILD_TYPE STREQUAL "Release")
  add_compile_options(
    -O3 # Enable aggressive optimizations
    -DNDEBUG # Disable assertions
    -march=native # Generate code optimized for the host CPU architecture
    -funroll-loops # Unroll loops to improve instruction-level parallelism
    -finline-functions # Inline small functions for performance improvement
  )

  # Define a preprocessor macro for release builds
  target_compile_definitions(Ravi PUBLIC RV_RELEASE)
  add_compile_definitions(Ravi PUBLIC RV_RELEASE)
  if(NOT APPLE)
    # Strip symbols in release builds
    set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} -s -fuse-ld=lld -flto")
    set(CMAKE_EXE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE} -s -fuse-ld=lld -flto")
  endif()
endif()