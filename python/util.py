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
