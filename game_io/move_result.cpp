#include "move_result.h"

move_result::move_result(Json::Value root, int player_number) {
    this->set_move_result(root, player_number);
}

void move_result::set_move_result(Json::Value root, int player_number) {
    this->by = root["id"].asInt();
    this->card = root["card"].asInt();

    if(this->by == player_number) {
        this->iwon = true;
    } else {
        this->iwon = false;
    }
}
