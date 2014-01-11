.PHONY: all

all: libjson_socket.so

INCLUDE_PATH=-I../jsoncpp/include
LIBRARY_PATH=-L../jsoncpp/src/lib_json
USELIBS=-ljson_cpp

all: libjson_socket.so

libjson_socket.so: json_socket.cpp json_socket.h
	g++ -g -fpic -shared $(INCLUDE_PATH) $(LIBRARY_PATH) $(USELIBS) -o libjson_socket.so json_socket.cpp

clean:
	-rm -f libjson_socket.so
