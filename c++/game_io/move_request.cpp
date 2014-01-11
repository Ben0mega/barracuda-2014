#include "move_request.h"

move_request::move_request(Json::Value root) {
    this->set_move_request(root);
}

void move_request::set_move_request(Json::Value root) {
    this->request = root["request"].asString();
    this->request_id = root["request_id"].asInt();
    this->remaining = root["remaining"].asDouble();
    this->state = new game_state(root["state"]);
}

move_request::~move_request() {
    delete this->state;
}
