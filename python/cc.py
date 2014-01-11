class CardCounter:
	cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
	
	def __init__(self):
		# there are 8 of each type of card
		#			   A  2  3  4  5  6  7  8  9  10 J  Q  K
		self.cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
	
	def shuffle():
		__init__()

	def cardRevealed(card):
		cardTallies[card] = cardTallies[card] - 1

	def probabilityOfCard(card):
		total = 0
		for tally in cardTallies:
			total += tally
		return cardTallies[card]/total

	def cardScore(card):
		total = 0
		number = 0
		for value in range(1, 13):
			number += cardTallies[value-1]
			total += value * cardTallies[value-1]
		return card - (total/number)

