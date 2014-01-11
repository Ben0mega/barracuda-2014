# Source files to compile with executable
file(GLOB_RECURSE JSONTESTRUNNER_SOURCE_FILES *.cpp)

ADD_EXECUTABLE(jsontestrunner ${JSONTESTRUNNER_SOURCE_FILES})
TARGET_LINK_LIBRARIES(jsontestrunner json_cpp)
