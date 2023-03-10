
class Companion():
    name = ''
    cost = 99999
    title = ''

    def __init__(self):
        for k,v in COMPANION_DECK.items():
            if type(self) == v:
                COMPANION_DECK[k] = None


    def __str__(self):
        return f"{self.name} ({self.title})"

    def join(self, entity):
        entity.companions.add(self)
        self._join(entity)

    def leave(self, entity):
        entity.companions.remove(self)
        self._leave(entity)

    def _leave(self, entity):
        pass
    def _join(self, entity):
        pass

    def win(self, relics):
        return False

class Scoundrel(Companion):
    cost = 100
    name = 'Jax'
    title = 'Scoundrel'
    def _leave(self, entity):
        entity.r -=1
        entity.JAX_BONUS = 0

    def _join(self, entity):
        entity.r +=1
        entity.JAX_BONUS = 5

class Doctor(Companion):
    cost = 100
    name = 'Dr. Efra'
    title = 'Galactic M.D.'

    def _leave(self, entity):
        entity.k -=1
        entity.EFRA_BONUS = 0

    def _join(self, entity):
        entity.k +=1
        entity.EFRA_BONUS = 1

class Mercenary(Companion):
    cost = 100
    name = 'Duncan'
    title = 'Ex-Mercenary'

    def _leave(self, entity):
        entity.h -=1
        entity.max_water -=1
        entity.DUNCAN_REROLL = 0

    def _join(self, entity):
        entity.h +=1
        entity.max_water +=1
        entity.DUNCAN_REROLL = 2

class Robot(Companion):
    cost = 150
    name = 'B3TA'
    title = 'Robot'

    def _leave(self, entity):
        entity.h = self.h
        entity.BETA_REROLL = 0

    def _join(self, entity):
        self.h = entity.h
        entity.h = max(entity.h - 1, 1)
        entity.BETA_REROLL = 2

class Mechanic(Companion):
    cost = 150
    name = 'Geronimo'
    title = 'Mechanic'

    def _leave(self, entity):
        entity.max_fuel -= 1
        entity.speed -= 1
        entity.GERONIMO_BONUS = 0

    def _join(self, entity):
        entity.max_fuel += 1
        entity.speed += 1
        entity.GERONIMO_BONUS = 1

class Seeker(Companion):
    cost = 200
    name = 'Host'
    title = 'Seeker'

    def _leave(self, entity):
        entity.k -= 1
        entity.max_stamina -= 2
        entity.max_water -= 1

    def _join(self, entity):
        entity.k += 1
        entity.max_stamina += 2
        entity.max_water += 1


class Cartographer(Companion):
    cost = 200
    name = 'Saffron'
    title = 'Cartographer'

    def _leave(self, entity):
        entity.SAFFRON_BONUS = 0
        pass

    def _join(self, entity):
        entity.SAFFRON_BONUS = 1
        pass
        #TODO: draw 2 explore


class HouseAgent(Companion):
    cost = 200
    name = 'Lady Marjorie'
    title = 'Minor House Agent'

    def _leave(self, entity):
        entity.r -= 1
        entity.max_stamina = self.stamina

    def _join(self, entity):
        self.stamina = entity.max_stamina
        entity.max_stamina = max(entity.max_stamina - 3, 1)
        entity.r += 1
        # TODO draw 2
        # TODO pick 2

class Mystic(Companion):
    cost = 0
    name = 'Kale'
    title = 'Mysteic'

    def win(self, relics):
        return relics >= 3

    def _leave(self, entity):
        entity.fame = entity.fame
        entity.h -= 1
        entity.k -= 1
        entity.r -= 1
        entity.max_stamina -= 2

    def _join(self, entity):
        self.fame = entity.fame
        entity.fame = 0
        entity.h += 1
        entity.k += 1
        entity.r += 1
        entity.max_stamina += 2

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
    ret = COMPANION_DECK[card.rank]
    return ret() if ret else ret
