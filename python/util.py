#ALGORITHM FUNCTIONS
def aheadByEnoughTricks(msg):
    return msg["state"]["your_tricks"] - msg["state"]["their_tricks"]  >= 1

def behind(msg):
    return msg["state"]["their_points"] - msg["state"]["your_points"] >= 2

def ahead(msg):
    return msg["state"]["your_points"] - msg["state"]["their_points"] >= 2

def opponentAboutToWin(msg):
    return msg["state"]["their_points"] == 9

def shouldStartChallenge(msg):
    if opponentAboutToWin(msg):
        return True
    if aheadByEnoughTricks(msg):
        return True
    #when behind, dark shrine
    if behind(msg):
       return True 
    if msg["state"]["your_points"] >= 8:
		cards = sorted(msg["state"]["hand"])
		index = int(len(cards)/2) + 1
		if float(sum(msg["state"]["hand"]))/len(msg["state"]["hand"]) > 9.4 or cards[index] > 3:
            return True
    if msg["state"]["their_tricks"] < 3:    # can you win the challenge?
        if float(sum(msg["state"]["hand"]))/len(msg["state"]["hand"]) > 9.4:
            return True
    return False

def shouldAcceptChallenge(msg):
    if ahead(msg):
        return False
    if opponentAboutToWin(msg):
        return True
    #when behind, dark shrine
    if behind(msg):
       return True 
    if aheadByEnoughTricks(msg):
        return True
    if msg["state"]["their_tricks"] < 3:    # can you win the challenge?
        if float(sum(msg["state"]["hand"]))/len(msg["state"]["hand"]) > 9.4:
            return True
    return False

def getNextHighestCard(msg, theirCard):
    card = min(msg["state"]["hand"])
    for a in msg["state"]["hand"]:
        if a < card or card <= theirCard:
            card = a
    return card

def getLeadCard(msg):
    cards = sorted(msg["state"]["hand"])
    index = int(len(cards)/2)
    card = cards[index];
    return card

def respondToPlay(msg, theirCard):
# if there is no highest card, it returns the lowest card
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
    return card

def testLeadCardTautology(msg):
    if msg["state"]["your_tricks"] == 2:
        return max(msg["state"]["hand"])

def testTrailCardTautology(msg, theirCard):
    nextHighest = getNextHighestCard(msg, theirCard)
    if nextHighest - theirCard == 1:
        return nextHighest
