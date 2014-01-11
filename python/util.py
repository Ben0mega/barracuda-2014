import math

#ALGORITHM FUNCTIONS
def aheadByEnoughTricks(msg):
    return msg["state"]["your_tricks"] - msg["state"]["their_tricks"]  >= 1

def behind(msg):
    return msg["state"]["their_points"] - msg["state"]["your_points"] >= 2

def ahead(msg):
    return msg["state"]["your_points"] - msg["state"]["their_points"] >= 2

def opponentAboutToWin(msg):
    return msg["state"]["their_points"] == 9

def tricksToWin(msg):
    handsLeft = 6 - msg["state"]["hand_id"]
    tiedGames = (msg["state"]["total_tricks"] - msg["state"]["their_tricks"]) - msg["state"]["your_tricks"]
    return (handsLeft - tiedGames)/2 + 1

def calculateHandScore(msg, deck):
    handScore = 0    
    for card in msg["state"]["hand"]:
        handScore += deck.cardScore(card)
    return handScore

def getNextHighestCard(msg, theirCard):
#Returns the min card when there is no next highest    
    minCard = min(msg["state"]["hand"])
    bestCard = max(msg["state"]["hand"])
    for a in msg["state"]["hand"]:
        if a < bestCard and a > theirCard:
            bestCard = a
    if bestCard < theirCard:
        return minCard    
    return bestCard

def canTie(msg, theirCard):
    if theirCard in msg["state"]["hand"]:    
        return True
    return False

def isLastCard(msg):
    return len(msg["state"]["hand"]) == 1

def averageHandValue(msg, min_val):    
    return float(sum(msg["state"]["hand"]))/len(msg["state"]["hand"]) >= min_val

def neededToWin(msg):
    return math.ceil(len(msg["state"]["hand"]) + msg["state"]["their_points"] + msg["state"]["your_points"] + 1 / 2)

def count_num_card(msg, card_val):
    return len( [ a for a in msg["state"]["hand"] if a >= card_val])

def shouldStartChallenge(msg, deck):
    if testShouldChallengeTautology(msg):
         return True

     #if calculateHandScore(msg, deck) > 0.5:
     #    return True

    if opponentAboutToWin(msg):
        return True
     #if aheadByEnoughTricks(msg):
     #    return True
    if msg["state"]["your_tricks"]+count_num_card(msg, 11) >= neededToWin(msg):
         return True
    #when behind, dark shrine
    if behind(msg):
        #TODO: make this a ratio with regards to how far each player is from winning
        if calculateHandScore(msg, deck) > 8:
           return True 
    
    #if len(msg["state"]["hand"]) == 1:
        #return True

    if isLastCard(msg):
        return False
    if calculateHandScore(msg, deck) > 9.5:
        if msg["state"]["their_tricks"] == 2 and "card" in msg["state"].keys() and msg["state"]["card"] > max(msg["state"]["hand"]):
            return False
        return True

    if msg["state"]["your_points"] == 9:
        if calculateHandScore(msg, deck) > 10:
                return True
        
    if calculateHandScore(msg, deck) > 10:
        if msg["state"]["their_tricks"] == (neededToWin(msg)-1) and "card" in msg["state"].keys() and msg["state"]["card"] > max(msg["state"]["hand"]):
            return False
        return True

    if (msg["state"]["your_points"] - msg["state"]["their_points"]) > neededToWin(msg):
        if calculateHandScore(msg, deck) > 9.7:
            return True
    if msg["state"]["their_tricks"] < neededToWin(msg):    # can you win the challenge?
        if msg["state"]["their_tricks"] == (neededToWin(msg)-1) and "card" in msg["state"].keys() and msg["state"]["card"] > max(msg["state"]["hand"]):
            return False
        if calculateHandScore(msg, deck) > 10.2 and msg["state"]["their_tricks"]+count_num_card(msg, 7) < neededToWin(msg):
            return True
    return False

def shouldAcceptChallenge(msg, deck):
    if testAcceptChallengeTautology(msg):
        return True

     #if calculateHandScore(msg, deck) > 0.5:
     #    return True
    
    if ahead(msg):
        return False
    if opponentAboutToWin(msg):
        return True
    #when behind, dark shrine
    if behind(msg):
        if calculateHandScore(msg, deck) > 10: #averageHandValue(msg, 9.4):
           return True 
    if msg["state"]["your_tricks"]+count_num_card(msg, 11) >=(neededToWin(msg)-msg["state"]["your_tricks"]):
         return True
    if msg["state"]["your_points"] == 9 and count_num_card(msg, 11) >= (neededToWin(msg)-msg["state"]["your_tricks"]):
        return True
    if isLastCard(msg):
        return False
    return False



def getLeadCard(msg):
    tautology = testLeadCardTautology(msg)
    if tautology != None:
        return tautology
    
    cards = sorted(msg["state"]["hand"])
    index = int(len(cards)/2)
    if len(cards) > 0 and len(cards) % 2 == 0:
        index -= 1
    card = cards[index];
    return card

def respondToPlay(msg, theirCard):
# if there is no highest card, it returns the lowest card
    tautology = testTrailCardTautology(msg, theirCard)
    if tautology != None:
        return tautology
    
    if msg["state"]["your_tricks"] == 2 and max(msg["state"]["hand"]) > theirCard:
        for a in sorted(msg["state"]["hand"]):
            if a > theirCard:
                return a
    
    card = min(msg["state"]["hand"])
    if (theirCard - card) >= 5 and msg["state"]["their_tricks"] < 2:
        return card

    for a in msg["state"]["hand"]:
        if card < theirCard and a == theirCard:
            card = theirCard
        elif a > theirCard:
            if a < card or card <= theirCard:
                card = a
    if (theirCard - min(msg["state"]["hand"])) > 2 and (card - theirCard) > 3 and msg["state"]["their_tricks"] < 2:
        card = min(msg["state"]["hand"])

    if canTie(msg, theirCard) and card < theirCard:
        return theirCard

    return card

def testLeadCardTautology(msg):
    if msg["state"]["your_tricks"] == 2:
        return max(msg["state"]["hand"])

def testTrailCardTautology(msg, theirCard):
    nextHighest = getNextHighestCard(msg, theirCard)
    if nextHighest - theirCard == 1:
        return nextHighest

def testAcceptChallengeTautology(msg):
    cards = sorted(msg["state"]["hand"])
    if cards[0] == 13 and cards[-1] == 13 and len(cards) + msg["state"]["your_tricks"] >= 3:
        return True
    if msg["state"]["your_tricks"] == 3:
        return True
    if msg["state"]["your_tricks"] == 2 and "card" in msg["state"].keys() and msg["state"]["card"] < max(msg["state"]["hand"]):
        return True
    return False

def testShouldChallengeTautology(msg):
    cards = sorted(msg["state"]["hand"])
    if cards[0] == 13 and cards[-1] == 13 and len(cards) + msg["state"]["your_tricks"] >= 3:
        return True
    if msg["state"]["your_tricks"] == 3:
        return True
    if msg["state"]["your_tricks"] == 2 and "card" in msg["state"].keys() and msg["state"]["card"] < max(msg["state"]["hand"]):
        return True
    return False

