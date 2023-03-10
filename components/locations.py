from . import tile_types
from . import explorations

class Location():
    level = 2
    size = 1
    desert = 0
    xp = 1
    tile = tile_types.error
    traversable = True
    can_visit = False

    def __init__(self, x, y, level=None, deck=None):
        self.x = x
        self.y = y
        if level: self.level = level

    def can_explore(self, entity):
        return True

    def explore(self, entity):
        pass

    def populate(self, deck):
        pass

    def __str__(self):
        if hasattr(self, "name"):
            return self.name
        t = type(self).__name__.replace("_", " ").title()
        if t.endswith(('1','2')):
            t = t[:-1]
        if self.level:
            t += f': {self.level}'

        return t

class Desert(Location):
    level  = 3
    tile = tile_types.desert

    def __init__(self, x, y, level=None, deck=None):
        super().__init__(x,y,level)
        if deck: self.populate(deck)

    def can_explore(self, entity):
        if self.xp > 0:
            return True
        if self.xp > -1 and hasattr(entity, "SMUGGLER_L1"):
            return True
        return True

    def explore(self, entity):
        if self.xp == 0 and hasattr(entity, "SMUGGLER_L1"):
            return self.do_smuggler_explore
        return self.do_desert_explore

    def populate(self, deck):
        card = deck.top
        self.do_desert_explore = explorations.DESERT_EXPLORATIONS[card.black][card.rank]
        self.do_smuggler_explore = explorations.DESERT_EXPLORATIONS[card.black][card.rank] #TODO
        pass

class NonTraversable(Location):
    level = 3
    tile = tile_types.nontraversable
    traversable = False

    def can_explore(self, entity):
        return self.xp > 0

    def explore(self, entity):
        return self.encounter

class Unique(Location):
    level = 2
    tile = tile_types.unique

    def can_explore(self, entity):
        return self.xp > 0

    def explore(self, entity):
        return self.encounter

class GuildUnique(Location):
    tile = tile_types.explorable

    def __init__(self,x,y,guild,level=None):
        super().__init__(x,y,level=level)
        self.guild = guild
        self.quest_level = guild.level

    def can_explore(self,entity):
        return entity.quest_guild ==self.guild and self.guild.level == self.quest_level

    def explore(self, entity):
        return self.encounter


class Settlement(Location):
    level = 2
    xp = 3
    tile = tile_types.settlement
    can_visit = True

    def __init__(self, x, y, level=None, deck=None):
        super().__init__(x,y,level)
        self.items = list()
        self.guild = None
        self.companion = None
        if deck: self.populate(deck)

    def populate(self, deck):
        from . import equipment, guilds, companions
        for i in range(deck.bottom.value // 3):
            i = equipment.draw(deck.top)
            if i:
                self.items.append(i)
            else:
                break
        # NB call constructor that is returned...
        self.guild = guilds.draw(deck.bottom)
        self.companion = companions.draw(deck.bottom)

    def can_explore(self, entity): return False
    # Settlements are explored via visiting


class Home(Settlement):
    pass


class Explorable(Location):
    tile = tile_types.explorable
    def __init__(self, x, y, level=None, deck=None):
        super().__init__(x,y,level)
        if not level and deck:
            card2 = deck.top
            if card2.major:
                self.level = 2
            elif card2.value > 10:
                self.level = 3
            else :
                self.level = 1

    def can_explore(self, entity):
        return self.xp > 0

    def explore(self, entity):
        return self.encounter

## Revealables:

class crashed_spaceship1(Explorable):
    desert = 4
    encounter = explorations.captains_log

class crashed_spaceship2(Explorable):
    desert = 4
    encounter = explorations.engineers_log


class oasis_settlement1(Settlement):
    desert = 2

class oasis_settlement2(Settlement):
    desert = 2


class merchant_outpost1(Settlement):
    desert = 2

class merchant_outpost2(Settlement):
    desert = 2


class abandoned_harvester1(Explorable):
    desert = 3
    encounter = explorations.spices_once_flowed

class abandoned_harvester2(Explorable):
    desert = 3
    encounter = explorations.gone_with_the_desert_winds


class research_outpost1(Explorable):
    desert = 3
    encounter = explorations.researchers_score

class research_outpost2(Explorable):
    desert = 3
    encounter = explorations.scientists_working


class gorge1(NonTraversable):
    size = 3
    desert = 0
    encounter = explorations.a_long_way_down

class gorge2(NonTraversable):
    size = 3
    desert = 0
    encounter = explorations.an_even_longer_way


class vehicle_scrapyard1(Explorable):
    desert = 2
    encounter = explorations.credits_unpaid

class vehicle_scrapyard2(Explorable):
    desert = 2
    encounter = explorations.glider_transports


class cartogropher_lookout1(Explorable):
    desert = 3
    encounter = explorations.a_friendly_keeper

class cartogropher_lookout2(Explorable):
    desert = 3
    encounter = explorations.a_long_and_quiet_view


class sand_pit1(NonTraversable):
    desert = 3
    encounter = explorations.that_sinking_feeling

class sand_pit2(NonTraversable):
    desert = 3
    encounter = explorations.down_the_drain


class old_battlefield1(Explorable):
    size = 2
    desert = 2
    encounter = explorations.battlefield_spoils

class old_battlefield2(Explorable):
    size = 2
    desert = 2
    encounter = explorations.buried_memories


class forgotten_guild_hall1(Unique):
    desert = 5
    encounter = explorations.untouched_relics_of_the_past

class forgotten_guild_hall2(Unique):
    desert = 5
    encounter = explorations.abandoned_and_worn_to_time


class ecological_stations1(Unique):
    size = 3
    desert = 0
    encounter = explorations.operation_restore_eridoor

class ecological_stations2(Unique):
    size = 3
    desert = 0
    encounter = explorations.tour_the_facility


class chrome_dome1(Unique):
    desert = 2
    encounter = explorations.cracked_shell

class chrome_dome2(Unique):
    desert = 2
    encounter = explorations.encrypted_security


#

class giant_snake_skeleton1(Explorable):
    size = 2
    desert = 6
    encounter = explorations.jaws_of_razors

class giant_snake_skeleton2(Explorable):
    size = 2
    desert = 6
    encounter = explorations.belly_of_the_beast


class moisture_farm1(Settlement):
    desert = 3

class moisture_farm2(Settlement):
    desert = 3


class trader_settlement1(Settlement):
    desert = 2

class trader_settlement2(Settlement):
    desert = 2


class weather_tower1(Explorable):
    desert = 6
    encounter = explorations.recording_weather_data

class weather_tower2(Explorable):
    desert = 6
    encounter = explorations.damaged_relay


class mining_shaft1(Explorable):
    desert = 1
    encounter = explorations.miners_bounty

class mining_shaft2(Explorable):
    desert = 1
    encounter = explorations.credit_payment_machine


class rock_cliffs1(NonTraversable):
    size = 4
    desert = 2
    encounter = explorations.sanded_down_over_time

class rock_cliffs2(NonTraversable):
    size = 4
    desert = 2
    encounter = explorations.never_ending_height


class sunken_outpost1(Explorable):
    desert = 1
    encounter = explorations.tip_of_the_sunken_tower

class sunken_outpost2(Explorable):
    desert = 1
    encounter = explorations.safe_haven


class settlement_ruins1(Explorable):
    size = 2
    desert = 4
    encounter = explorations.scattered_ruins

class settlement_ruins2(Explorable):
    size = 2
    desert = 4
    encounter = explorations.barely_standing_structures


class impact_crater1(NonTraversable):
    desert = 0
    encounter = explorations.a_big_hole

class impact_crater2(NonTraversable):
    desert = 0
    encounter = explorations.an_even_bigger_hole


class glider_station1(Explorable):
    desert = 4
    encounter = explorations.bottom_of_the_tank

class glider_station2(Explorable):
    desert = 4
    encounter = explorations.glider_mods_galore


class escape_pods1(Unique):
    desert = 2
    encounter = explorations.empty_escape_pods

class escape_pods2(Unique):
    desert = 2
    encounter = explorations.sealed_for_your_protection


class crumbling_factory1(Unique):
    desert = 6
    encounter = explorations.warehouse_wonders

class crumbling_factory2(Unique):
    desert = 6
    encounter = explorations.rusted_robotics_workshop


class desert_lighthouse1(Unique):
    desert = 8
    encounter = explorations.guiding_light_keeper

class desert_lighthouse2(Unique):
    desert = 8
    encounter = explorations.lost_ways



# Wild cards

class onyx_pillars(Unique):
    desert = 4
    xp = 3
    encounter = explorations.the_heart_of_eridoor

class floating_obelisk(Unique) :
    desert = 3
    xp = 3
    encounter = explorations.the_sound_of_eridoor




REVEAL_DECK = {

  'AC': crashed_spaceship1,
  '2C': oasis_settlement1,
  '3C': merchant_outpost1,
  '4C': abandoned_harvester1,
  '5C': research_outpost1,
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
  '5S': research_outpost2,
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


def draw(deck, x, y, redraw=False):
    card = deck.top
    ret = REVEAL_DECK[card](x,y,deck=deck)
    if redraw and isinstance(ret, (Desert, NonTraversable)):
        ret = REVEAL_DECK[card](x,y,deck=deck)
    if isinstance(ret, Unique):
        REVEAL_DECK[card] = Desert
    return ret




