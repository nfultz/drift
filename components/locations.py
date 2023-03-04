
class Location():
    level = 2

    def can_explore(self, entity):
        return True

    def explore(self, entity):
        pass

class Desert(Location):
    level  = 3

class NonTraversable(Location):
    level = 3

    def can_explore(self, entity):
        return hasattr(entity, "PATHFINDER")

class Unique(Location):
    level = 2

class Settlement(Location):
    level = 2

class Explorable(Location):
    def __init__(self):
        super().__init__()

## Revealables:

class crashed_spaceship1(Explorable): pass
class crashed_spaceship2(Explorable): pass

class oasis_settlement1(Settlement): pass
class oasis_settlement2(Settlement): pass

class merchant_outpost1(Settlement): pass
class merchant_outpost2(Settlement): pass

class abandoned_harvester1(Explorable): pass
class abandoned_harvester2(Explorable): pass

class research_output1(Explorable): pass
class research_output2(Explorable): pass

class gorge1(NonTraversable): pass
class gorge2(NonTraversable): pass

class vehicle_scrapyard1(Explorable): pass
class vehicle_scrapyard2(Explorable): pass

class cartogropher_lookout1(Explorable): pass
class cartogropher_lookout2(Explorable): pass

class sand_pit1(NonTraversable): pass
class sand_pit2(NonTraversable): pass

class old_battlefield1(Explorable): pass
class old_battlefield2(Explorable): pass

class forgotten_guild_hall1(Unique): pass
class forgotten_guild_hall2(Unique): pass

class ecological_stations1(Unique): pass
class ecological_stations2(Unique): pass

class chrome_dome1(Unique): pass
class chrome_dome2(Unique): pass

#

class giant_snake_skeleton1(Explorable): pass
class giant_snake_skeleton2(Explorable): pass

class moisture_farm1(Settlement): pass
class moisture_farm2(Settlement): pass

class trader_settlement1(Settlement): pass
class trader_settlement2(Settlement): pass

class weather_tower1(Explorable): pass
class weather_tower2(Explorable): pass

class mining_shaft1(Explorable): pass
class mining_shaft2(Explorable): pass

class rock_cliffs1(NonTraversable): pass
class rock_cliffs2(NonTraversable): pass

class sunken_outpost1(Explorable): pass
class sunken_outpost2(Explorable): pass

class settlement_ruins1(Explorable): pass
class settlement_ruins2(Explorable): pass

class impact_crater1(NonTraversable): pass
class impact_crater2(NonTraversable): pass

class glider_station1(Explorable): pass
class glider_station2(Explorable): pass

class escape_pods1(Unique): pass
class escape_pods2(Unique): pass

class crumbling_factory1(Unique): pass
class crumbling_factory2(Unique): pass

class desert_lighthouse1(Unique): pass
class desert_lighthouse2(Unique): pass


# Wild cards

class onyx_pillars(Unique): pass
class floating_obelisk(Unique) : pass



REVEAL_DECK = {

  'AC': crashed_spaceship1,
  '2C': oasis_settlement1,
  '3C': merchant_outpost1,
  '4C': abandoned_harvester1,
  '5C': research_output1,
  '6C': gorge1,
  '7C': vehicle_scrapyard1,
  '8C': cartogropher_lookout1,
  '9C': sand_pit1,
  '0C': old_battlefield1,
  'JC': forgotten_guild_hall1,
  'QC': ecological_stations1,
  'KC': chrome_dome1,

  'AD': giant_snake_skeleton1,
  '2D': moisture_farm1,
  '3D': trader_settlement1,
  '4D': weather_tower1,
  '5D': mining_shaft1,
  '6D': rock_cliffs1,
  '7D': sunken_outpost1,
  '8D': settlement_ruins1,
  '9D': impact_crater1,
  '0D': glider_station1,
  'JD': escape_pods1,
  'QD': crumbling_factory1,
  'KD': desert_lighthouse1,

  'AS': crashed_spaceship2,
  '2S': oasis_settlement2,
  '3S': merchant_outpost2,
  '4S': abandoned_harvester2,
  '5S': research_output2,
  '6S': gorge2,
  '7S': vehicle_scrapyard2,
  '8S': cartogropher_lookout2,
  '9S': sand_pit2,
  '0S': old_battlefield2,
  'JS': forgotten_guild_hall2,
  'QS': ecological_stations2,
  'KS': chrome_dome2,

  'AH': giant_snake_skeleton2,
  '2H': moisture_farm2,
  '3H': trader_settlement2,
  '4H': weather_tower2,
  '5H': mining_shaft2,
  '6H': rock_cliffs2,
  '7H': sunken_outpost2,
  '8H': settlement_ruins2,
  '9H': impact_crater2,
  '0H': glider_station2,
  'JH': escape_pods2,
  'QH': crumbling_factory2,
  'KH': desert_lighthouse2,


  'WS': onyx_pillars,
  'WH': floating_obelisk
}


def draw(deck):
    card = deck.top
    ret = REVEAL_DECK[card]()
    if isinstance(ret, Unique):
        REVEAL_DECK[card] = Desert
    if isinstance(ret, Explorable):
        card2 = deck.top
        if card2.major:
            ret.level = 2
        elif card2.value > 10:
            ret.level = 3
        else :
            ret.level = 1
    return ret




