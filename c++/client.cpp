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
int choice;
int won;

double cost(int opp_c, vector<int>& hand, int choice, game_state& gs){
	int sum = 0;
	for(auto c : hand) sum+=c;
	
	double ret = double(sum)/hand.size() - double(sum-choice)/(hand.size()-1);
	if(opp_c > choice){
		ret += gs.their_tricks;
	} else if(opp_c < choice){
		ret+= -1.0;
	}

	return ret;
}

void client::error(error_msg* err) {
    cout << "error: " << err->message << endl;
}

move_response* client::move(move_request* req) {
	auto value = 0;
	for(auto card : req->state->hand){
		value+=card;
	}
	if (value > 50 && req->state->can_challenge) {
		cerr << "Challenging!\n";
		return new offer_challenge();
	}

	choice = req->state->hand.front();
	if(req->state->opp_lead &&  req->state->card){
		int opp_card = req->state->card;
		auto min_cost = cost(opp_card, req->state->hand, req->state->hand.front(), *req->state);
		for(auto card : req->state->hand){
			auto temp_cost = cost(opp_card, req->state->hand, card, *req->state);
			if(temp_cost < min_cost){
				min_cost = temp_cost;
				choice = card;
			}
		}
		if(req->state->their_tricks >= 2 && choice < opp_card){
			for(auto c : req->state->hand) choice = max(c, choice);
		}

		cerr << "They played " << opp_card << '\n';
		cerr << "We respond: ";
		if(choice > opp_card) won = 1;
		else if(choice < opp_card) won = -1;
		else won = 0;
	
	} else {
		won = 0;
		int choice2 = 14;
		for(auto card : req->state->hand){
			if(card > 7) choice2 = min(choice2, card);
			choice = max(choice, card);
		}
		if(req->state->their_tricks < 2 && choice2 != 14){
			choice = choice2;
		}
		/*int sum = 0;
		for(auto card : req->state->hand) sum+= card;
		
		if(sum < 40){
			for(auto card: req->state->hand){
				choice = min(choice, card);
			}
		}*/
		cerr << "We play: ";
	}
	cerr << choice << '\n';
	cerr << "I am: " << req->state->player_number << '\n';
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
	int count = 0;
	for(auto c : hand){
		if(c == max) count++;
	}
	return count == num;
}

challenge_response* client::challenge(move_request* req) {
	auto tricks_won = req->state->your_tricks;
	if (tricks_won >= 3) {
		cerr << "Challenge Accepted!\n";
		return new challenge_response(true);
	}

	if (tricks_won == 2 && highest_num_cards(1, req->state->hand )) {
		cerr << "Challenge Accepted!\n";
		return new challenge_response(true);
	}

	if (tricks_won == 1 && highest_num_cards(2, req->state->hand)) {
		cerr << "Challenge Accepted!\n";
		return new challenge_response(true);
	}

	if (tricks_won == 0 && highest_num_cards(3, req->state->hand)) {
		cerr << "Challenge Accepted!\n";
		return new challenge_response(true);
	}

	cerr << "Challenge Rejected!\n";
	return new challenge_response(false);
}

void client::server_greeting(greeting* greet) {
    cout << "Connected to server." << endl;
}

void client::game_over(game_result* r) {
	if(!r->iwon) {
		cerr << "WINNER!\n";
	} else {
		cerr << "LOST!!!\n";
	}
    // left blank for you
}

void client::trick_done(move_result* r) {
    // left blank for you
	if(won == 1 || (won == 0 && choice > r->card)) {
		cerr << "WINNER! with card " << r->card <<"\n";
	} else if( won == -1 || (won == 0 && choice < r->card)){
		cerr << "LOST!!! with card " << r->card <<"\n";
	} else cerr << "TIE!\n";
	
}

void client::hand_done(move_result* r) {
    // left blank for you
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
