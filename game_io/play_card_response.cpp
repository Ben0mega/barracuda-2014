#include "play_card_response.h"

play_card_response::play_card_response(int card) {
    this->set_type("play_card");
    this->json_root["response"]["card"] = card;
}
