#pragma once

#include "json_response.h"

class challenge_response : public json_response {
    public:
        challenge_response(bool);
};
