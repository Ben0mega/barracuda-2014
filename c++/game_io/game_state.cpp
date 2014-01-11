#include "game_state.h"

game_state::game_state(Json::Value state) {
    this->set_game_state(state);
}

void game_state::set_game_state(Json::Value state) {
    for(unsigned int i = 0; i < state["hand"].size(); i++) {
        this->hand.push_back(state["hand"][i].asInt());
    }

    this->hand_id = state["hand_id"].asInt();
    this->game_id = state["game_id"].asInt();
    this->your_tricks = state["your_tricks"].asInt();
    this->their_tricks = state["their_tricks"].asInt();
    this->can_challenge = state["can_challenge"].asBool();
    this->in_challenge = state["in_challenge"].asBool();
    this->total_tricks = state["total_tricks"].asInt();
    this->your_points = state["your_points"].asInt();
    this->opponent_id = state["opponent_id"].asInt();
    this->their_points = state["their_points"].asInt();
    this->player_number = state["player_number"].asInt();

    if(state.isMember("card")) {
        this->opp_lead = true;
        this->card = state["card"].asInt();
    }
}
