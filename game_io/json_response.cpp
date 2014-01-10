#include "json_response.h"

void json_response::set_type(string type) {
    this->json_root["type"] = "move";
    this->json_root["response"]["type"] = type;
}

void json_response::set_request_id(int req_id) {
    this->json_root["request_id"] = req_id;
}
