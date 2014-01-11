#pragma once

#include "json/json.h"

class move_result {
    public:
        move_result(Json::Value, int);
        void set_move_result(Json::Value, int);
        int by;
        int card;
        int iwon;
};
