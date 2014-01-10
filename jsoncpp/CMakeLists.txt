cmake_minimum_required (VERSION 2.6)
project (jsoncpp)

# Read out version
file (STRINGS "version" JSON_CPP_VERSION)

configure_file (
	"${PROJECT_SOURCE_DIR}/version.h.in"
	"${PROJECT_SOURCE_DIR}/include/json/version.h"
)

# Define Executable Output Directory
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})

# Include our configuration header
include_directories(${CMAKE_SOURCE_DIR}/include)

# Build the different applications
add_subdirectory (src)

#install the includes
add_subdirectory (include)
