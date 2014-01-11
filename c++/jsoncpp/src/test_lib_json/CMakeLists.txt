# Source files to compile with executable
file(GLOB_RECURSE TESTLIBJSON_SOURCE_FILES *.cpp)

ADD_EXECUTABLE(test_lib_json ${TESTLIBJSON_SOURCE_FILES})
TARGET_LINK_LIBRARIES(test_lib_json json_cpp)
