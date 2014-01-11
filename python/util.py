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
	for a in msg["state"]["hand"]:
		if card < theirCard and a == theirCard:
			card = theirCard
		elif a > theirCard:
			if a < card or card <= theirCard:
				card = a
	return card

def testLeadCardTautology(msg):
	if msg["state"]["your_tricks"] == 2:
		return max(msg["state"]["hand"])
	

def testTrailCardTautology(msg, theirCard):
	nextHighest = getNextHighestCard(msg, theirCard)
	if nextHighest - theirCard == 1:
		return nextHighest


