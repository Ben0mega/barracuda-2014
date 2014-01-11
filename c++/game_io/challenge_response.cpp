#include "challenge_response.h"

challenge_response::challenge_response(bool challenge) {
    if(challenge) {
        this->set_type("accept_challenge");
    } else {
        this->set_type("reject_challenge");
    }
}
