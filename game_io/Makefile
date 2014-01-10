.PHONY: all .cpp.o

CXX=game_io.cpp \
	challenge_response.cpp \
	error_msg.cpp \
	game_result.cpp \
	game_state.cpp \
	greeting.cpp \
	json_response.cpp \
	move_request.cpp \
	move_result.cpp \
	offer_challenge.cpp \
	play_card_response.cpp

OBJECTS=$(CXX:.cpp=.o)

INCLUDE_PATH=-I../jsoncpp/include \
			 -I../json_socket

LIBRARY_PATH=-L../json_socket \
			 -L../jsoncpp/src/lib_json
USELIBS=-ljson_cpp \
		 -ljson_socket

all: libgame_io.so

libgame_io.so: $(OBJECTS)
	g++ -g -shared -Wall -fpic $(INCLUDE_PATH) $(LIBRARY_PATH) $(USELIBS) $(OBJECTS) -o $@

.cpp.o:
	g++ -g -c -Wall -fpic $(INCLUDE_PATH) $(LIBRARY_PATH) $< -o $@

clean:
	-rm -f *.o *.so
