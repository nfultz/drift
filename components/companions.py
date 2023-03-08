
class Companion():
    name = ''
    cost = 99999
    title = ''
    def __str__(self):
        return f"{self.name} ({self.title})"

class Scoundrel(Companion):
    cost = 100
    name = 'Jax'
    title = 'Scoundrel'

class Doctor(Companion):
    cost = 100
    name = 'Dr. Efra'
    title = 'Galactic M.D.'

class Mercenary(Companion):
    cost = 100
    name = 'Duncan'
    title = 'Ex-Mercenary'

class Robot(Companion):
    cost = 150
    name = 'B3TA'
    title = 'Robot'

class Mechanic(Companion):
    cost = 150
    name = 'Geronimo'
    title = 'Mechanic'

class Seeker(Companion):
    cost = 200
    name = 'Host'
    title = 'Seeker'
class Cartographer(Companion):
    cost = 200
    name = 'Saffron'
    title = 'Cartographer'
class HouseAgent(Companion):
    cost = 200
    name = 'Lady Marjorie'
    title = 'Minor House Agent'

class Mystic(Companion):
    cost = 0
    name = 'Kale'
    title = 'Mysteic'

COMPANION_DECK = {
  'A' : Scoundrel,
  '2' : Scoundrel,
  '3' : Doctor,
  '4' : Doctor,
  '5' : Mercenary,
  '6' : Mercenary,
  '7' : Robot,
  '8' : Robot,
  '9' : Mechanic,
  '0' : Mechanic,
  'J' : Seeker,
  'Q' : Cartographer,
  'K' : HouseAgent,
  'W' : Mystic
  }

def draw(card):
    global COMPANION_DECK
    ret = COMPANION_DECK[card.rank]
    COMPANION_DECK = {k: None if v is ret else v for k,v in COMPANION_DECK.items()}
    return ret
