#!/usr/bin/python

# This should work in both recent Python 2 and Python 3.

import socket
import json
import struct
import time
import sys
from util import *
from cc import *

s = 0

#DUMB FUNCTIONS
def canChallenge(msg):
    if msg["state"]["can_challenge"] == True:
        return True
    return False

def sendChallenge(msg):
    if canChallenge(msg):
        s.send({"type": "move", "request_id": msg["request_id"], 
            "response": {"type": "offer_challenge"}})
    else:
        print("ERROR: can't actually send the challenge, stupid")
        exit(1)

def acceptChallenge(msg):
    s.send({"type": "move", "request_id": msg["request_id"],
        "response": {"type": "accept_challenge"}})

def rejectChallenge(msg):
    s.send({"type": "move", "request_id": msg["request_id"],
        "response": {"type": "reject_challenge"}})

def playCard(msg, card):
    s.send({"type": "move", "request_id": msg["request_id"],
        "response": {"type": "play_card", "card": card}})


def sample_bot(host, port):
    global s 
    s = SocketLayer(host, port)

    gameId = None

    while True:
        msg = s.pump()
        if msg["type"] == "error":
            print("The server doesn't know your IP. It saw: " + msg["seen_host"])
            sys.exit(1)
        elif msg["type"] == "request":
            #NEW GAME
            if msg["state"]["game_id"] != gameId:
                gameId = msg["state"]["game_id"]
                deck = CardCounter()
                print("New game started: " + str(gameId))
            
            #SHOULD CHALLENGE
            if shouldStartChallenge(msg) and canChallenge(msg):
                sendChallenge(msg)    
            
            #REQUEST PLAY A CARD
            if msg["request"] == "request_card":
                
                #YOU GO SECOND
                if "card" in msg["state"].keys():
                    cardToPlay = respondToPlay(msg, msg["state"]["card"])  

                #YOU GO FIRST
                else:
                    cardToPlay = getLeadCard(msg)
                playCard(msg, cardToPlay)
            
            #THEY CHALLENGE YOU
            elif msg["request"] == "challenge_offered":
                if shouldAcceptChallenge(msg):
                    acceptChallenge(msg);
                else:
                    rejectChallenge(msg);
        #elif msg["type"] == "result":
            #if msg["result"]["type"] == "trick_won":

            #elif msg["result"            
    
        elif msg["type"] == "greetings_program":
            print("Connected to the server.")

def loop(player, *args):
    while True:
        try:
            player(*args)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(repr(e))
        time.sleep(10)

class SocketLayer:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.s.connect((host, port))

    def pump(self):
        """Gets the next message from the socket."""
        sizebytes = self.s.recv(4)
        (size,) = struct.unpack("!L", sizebytes)

        msg = []
        bytesToGet = size
        while bytesToGet > 0:
            b = self.s.recv(bytesToGet)
            bytesToGet -= len(b)
            msg.append(b)

        msg = "".join([chunk.decode('utf-8') for chunk in msg])

        return json.loads(msg)

    def send(self, obj):
        """Send a JSON message down the socket."""
        b = json.dumps(obj)
        length = struct.pack("!L", len(b))
        self.s.send(length + b.encode('utf-8'))

    def raw_send(self, data):
        self.s.send(data)

if __name__ == "__main__":
    loop(sample_bot, "cuda.contest", 9999)
