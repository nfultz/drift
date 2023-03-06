
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
