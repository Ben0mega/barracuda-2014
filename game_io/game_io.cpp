#include "game_io.h"
#include <iostream>

game_mediator::game_mediator(game_player* player, json_socket* jsock) {
    this->player = player;
    this->jsock = jsock;
}

void game_mediator::start() {
    json_response* resp;
    string type;
    Json::Value root;

    while(1) {
        resp = NULL;
        root = this->jsock->recv_msg();
        type = root["type"].asString();

        if(type == "request") {
            move_request *req = new move_request(root);
            this->player_number = req->state->player_number;
            if(root["request"] == "request_card") {
                resp = player->move(req);
            } else if(root["request"] == "challenge_offered") {
                resp = player->challenge(req);
            } else {
                cout << "Unknown move request " << root["request"] << endl;
                cout << this->jsock->last_jsonstr << endl;
            }
            delete req;
        } else if(type == "greetings_program") {
            greeting *greet = new greeting(root);
            player->server_greeting(greet);
            delete greet;
        } else if(type == "error") {
            error_msg *err = new error_msg(root);
            player->error(err);
            delete err;
        } else if(type == "result") {
            string result_type = root["result"]["type"].asString();
            if(result_type == "trick_won" || result_type == "trick_tied") {
                move_result* res = new move_result(root["result"], this->player_number);
                player->trick_done(res);
                delete res;
            } else if(result_type == "hand_done") {
                move_result* res = new move_result(root["result"], this->player_number);
                player->hand_done(res);
                delete res;
            } else if(result_type == "game_won") {
                game_result* res = new game_result(root["result"], this->player_number);
                player->game_over(res);
                delete res;
            } else if(result_type == "accepted") {
            } else {
                cout << "Unknown result " << root["result"] << endl;
                cout << this->jsock->last_jsonstr << endl;
            }
        } else {
            cout << "Unknown type: " << type << " seen" << endl;
            cout << this->jsock->last_jsonstr << endl;
        }

        if(resp != NULL) {
            resp->set_request_id(root["request_id"].asInt());
            this->jsock->send_msg(resp->json_root);
            delete resp;
        }
    }
}
