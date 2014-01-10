#pragma once

#include "json/json.h"

class game_result {
    public:
        game_result(Json::Value, int);
        void set_game_result(Json::Value, int);
        int by;
        int iwon;
};
