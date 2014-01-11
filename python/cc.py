class CardCounter:
    total = 104    
    cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    
    def __init__(self):
        self.shuffle()

    def shuffle(self):
        # there are 8 of each type of card
        #                   A  2  3  4  5  6  7  8  9  10 J  Q  K
        self.cardTallies = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
        self.total = 104 

    def cardRevealed(self, card):
        self.total -= 1
        self.cardTallies[card-1] -= 1
        if self.cardTallies[card-1] < 0:
            print("ERROR: " + str(card))

    def probabilityOfCard(self, card):
        if total == 0:
            print("FUCK")
        return self.cardTallies[card-1]/total

    def probabilityOfHigher(self, card):
        prob = 0
        for card in {card-1, 12}
            prob += self.probabilityOfCard(card)
        return prob

    def cardScore(self, card):
        tally = 0
        for value in range(0, 12):
            tally += (value + 1) * self.cardTallies[value]
        if self.total == 0:
            print("SHIT")        
        return card - (tally/self.total)

