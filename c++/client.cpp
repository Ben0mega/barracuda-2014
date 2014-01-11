#ifndef _MSC_VER
#include <unistd.h>
#define SLEEP(x) sleep(x)
#else
#include <windows.h>
#define SLEEP(x) Sleep(x)
#endif

#include "client.h"
#include "json_socket/json_socket.h"
#include <algorithm>

int tricks_won = 0;

void client::error(error_msg* err) {
    cout << "error: " << err->message << endl;
}

move_response* client::move(move_request* req) {
	int choice = req->state->hand.front();
	if(req->state->opp_lead){
		int opp_card = req->state->card;
		for(auto card : req->state->hand){
			// if our card wins
			if(card > opp_card){
				//if our current choice loses...
				if(choice < opp_card) choice = card;
				//if our current choice wins, but is higher than card
				else choice = min(choice,card);
			} else if(card < opp_card){
				if(choice > opp_card) continue;
				choice = min(choice, card);
			}
		}
	} else {
		for(auto card : req->state->hand){
			choice = max(choice, card);
		}
	}
	for(auto it = req->state->hand.begin(); it != req->state->hand.end(); ++it){
		if(*it == choice){
			req->state->hand.erase(it);
			break;
		}
	}
	cerr << "Cards: ";
	for(auto card : req->state->hand){
		cerr << card << ',';
	}
	cerr << endl;
    return new play_card_response(choice);
}

bool highest_num_cards(int num, vector<int>& hand)
{
	int max = 13;
	for (int i = hand.size() - 1; i > num; --i) {
		if (hand[i] < max)
			return false;
	}
}

challenge_response* client::challenge(move_request* req) {
	if (tricks_won >= 3) {
		return new challenge_response(true);
	}

	sort(req->state->hand.begin(), req->state->hand.end());

	if (tricks_won == 2 && highest_num_cards(1, req->state->hand)) {
		return new challenge_response(true);
	}

	if (tricks_won == 1 && highest_num_cards(2, req->state->hand)) {
		return new challenge_response(true);
	}

	if (tricks_won == 0 && highest_num_cards(3, req->state->hand)) {
		return new challenge_response(true);
	}

	auto value = 0;
	for(auto card : req->state->hand){
		value+=card;
	}
	if(value*100/req->state->hand.size() > 9)
		return new challenge_response(true);
	return new challenge_response(false);
}

void client::server_greeting(greeting* greet) {
    cout << "Connected to server." << endl;
}

void client::game_over(game_result* r) {
	if(r->iwon) {
		cerr << "WINNER!\n";
	} else {
		cerr << "LOST!!!\n";
	}
    // left blank for you
}

void client::trick_done(move_result* r) {
    // left blank for you
	if(r->iwon) {
		++tricks_won;
	}
}

void client::hand_done(move_result* r) {
    // left blank for you
	if(r->iwon) {
		tricks_won = 0;
	}
}

int main(void) {
#ifdef _MSC_VER
	// Initialize Winsock
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 0), &wsaData);
#endif

    string server = "cuda.contest";
    for (;;) {
        try {
            json_socket contest_server = json_socket(server, "9999");

            client myclient = client();

            game_mediator game = game_mediator(&myclient, &contest_server);
            game.start();
        }
        catch (UnableToConnect) {
            cout << "Unable to connect. Waiting 10 seconds..." << endl;
        }
        catch (NotParseableJson) {
            cout << "Unparsable JSON encountered. Server probably hung up. Waiting 10 seconds..."
                 << endl;
        }
        SLEEP(10);
    }

    return 0;
}
