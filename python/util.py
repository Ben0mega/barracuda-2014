def getHighestCard(msg):
	maxCard = 0
	for card in msg["state"]["hand"]:
		if card > maxCard:
			maxCard = card
	return maxCard

def getNextHighestCard(msg, theirCard):
# if there is no highest card, it returns the lowest card
	minCard = 16
	bestCard = msg["state"]["hand"][0]
	for card in msg["state"]["hand"]:
		if card < minCard:
			minCard = card
		if card > theirCard and card < bestCard:
			bestCard = card
	if bestCard < theirCard:
		return minCard
	return bestCard

class CardCounter:
	cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
	
	def __init__():
		# there are 8 of each type of card
		#			   A  2  3  4  5  6  7  8  9  10 J  Q  K
		cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
	
	def shuffle():
		__init__()

	def cardRevealed(card):
		cardTallies[card] = cardTallies[card] - 1

	def probabilityOfCard(card):
		total = 0
		for tally in cardTallies:
			total += tally
		return cardTallies[card]/total
