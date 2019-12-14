from cards import Card
import random
class Deck:
    def __init__(self):
        self._cards = []
        self.populate()
        #print(self._cards)
    def populate(self):
        suits = ["hearts", "clubs", "diamonds", "spades"]
        numbers = [str(n) for n in range(2,11)] + ["Jack","Queen","King","Ace"]
        self._cards = [Card(s, n) for s in suits for n in numbers]
    def shuffle(self):
        random.shuffle(self._cards)
    def deal(self):
        return self._cards.pop()
    def return_card(self, card):
        if card in self._cards:
            print("Error card already in deck.")
        self._cards.append(card)
    def deck_count(self):
        c = 0
        for i in self._cards:
            c += 1
        return c
# Test Code Area
#d = Deck()
#print(str(d.deck_count()))
