#pragma once

#include "json/json.h"
#include <vector>

using namespace std;

class game_state {
    public:
        game_state(Json::Value);
        void set_game_state(Json::Value);
        vector<int> hand;
        int hand_id;
        int game_id;
        int your_tricks;
        int their_tricks;
        bool can_challenge;
        bool in_challenge;
        int total_tricks; //could be less than your_tricks+their_tricks if there have been ties
        int your_points;
        int opponent_id;
        int their_points;
        int player_number;
        bool opp_lead; //if true the opponent has lead a card and this->card will be set
        int card; //card the opponent has played if opp_lead is true
};
