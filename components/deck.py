import random


SUITS = "CDHS"
RANKS = "A234567890JQK"

class Card(str):

    @property
    def rank(self):
        return self[0]

    @property
    def suit(self):
        return self[1]

    @property
    def major(self):
        return self.suit in "HS"

    @property
    def red(self):
        return self.suit in "HD"

    @property
    def black(self):
        return self.suit in "CS"

    @property
    def value(self):
        if self.rank == 'W':
            return 14
        return 1 + RANKS.find(self.rank)

class Deck(list):

    def __init__(self):
        self += [Card(r+s) for s in SUITS for r in RANKS]
        self.append(Card("WS"))
        self.append(Card("WH"))
        self._top = len(self)
        self._bottom = 0

    def shuffle(self):
        random.shuffle(self)
        return self

    @property
    def drift(self):
        return (self._top - self._bottom) // 2

    @property
    def heat(self):
        temp = lambda x: x.value - 7
        x =  sum(map(temp, self[:self._bottom]), 100)
        y =  sum(map(temp, self[self._top - 1:]), 100)
        if x == y:
            x = x-2
        return sorted((x,y))

    @property
    def top(self):
        j = self._top - 1
        i = random.randrange(0, self._top)
        self[i], self[j] = self[j], self[i]

        self._top = self._top - 1
        if self._top == 0:
            self._top = len(self)

        return self[j]

    @property
    def bottom(self):
        j = self._bottom
        i = random.randrange(j, len(self))
        self[i], self[j] = self[j], self[i]

        self._bottom = self._bottom + 1
        if self._bottom == len(self):
            self._bottom = 0

        return self[j]







