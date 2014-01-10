#include "game_result.h"

game_result::game_result(Json::Value result, int player_number) {
    this->set_game_result(result, player_number);
}

void game_result::set_game_result(Json::Value result, int player_number) {
    this->by = result["by"].asInt();

    if(this->by == player_number) {
        this->iwon = true;
    } else {
        this->iwon = false;
    }
}
