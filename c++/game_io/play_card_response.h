#pragma once

#include "json_response.h"

class play_card_response : public move_response {
    public:
        play_card_response(int);
    private:
        int card;
};
