class CardCounter:
    cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    
    def __init__(self):
        # there are 8 of each type of card
        #               	A  2  3  4  5  6  7  8  9  10 J  Q  K
        self.cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    
    def shuffle(self):
        __init__(self)

    def cardRevealed(self, card):
        self.cardTallies[card-1] -= 1

    def probabilityOfCard(self, card):
        total = 0
        for tally in cardTallies:
            total += tally
        return self.cardTallies[card-1]/total

    def cardScore(self, card):
        total = 0
        number = 0
        for value in range(1, 13):
            number += self.cardTallies[value-1]
            total += value * self.cardTallies[value-1]
        return card - (total/number)

