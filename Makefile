.PHONY: all clean game_io json_socket jsoncpp clean_all

all: client

INCLUDE_PATH=-Igame_io \
			 -Ijson_socket \
			 -Ijsoncpp/include
LIBRARY_PATH=-Ljson_socket \
			 -Lgame_io \
			 -Ljsoncpp/src/lib_json
USELIBS=-lgame_io \
		 -ljson_socket \
		 -ljson_cpp

client: client.h client.cpp jsoncpp json_socket game_io
	g++ -g -std=c++0x -o $@ $(INCLUDE_PATH) $(LIBRARY_PATH) client.cpp $(USELIBS)

json_socket:
	cd json_socket && $(MAKE)

game_io:
	cd game_io && $(MAKE)

jsoncpp:
	cd jsoncpp && cmake -G "Unix Makefiles"
	cd jsoncpp && $(MAKE)

clean:
	-rm -f client

clean_all: clean
	cd json_socket && $(MAKE) clean
	cd game_io && $(MAKE) clean
	cd jsoncpp && $(MAKE) clean
