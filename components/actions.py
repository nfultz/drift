from __future__ import annotations

from typing import TYPE_CHECKING
import fractions
from . import locations

from tcod import event # :(event

class MixedFrac(fractions.Fraction):
    """
    A helper class for printing mixed fractions correctly.
    """

    def __str__(self):
        whole,space, n, slash, d = '','', '', '', ''
        i, j = divmod(self.numerator, self.denominator)

        if i != 0 or j == 0:
            whole = i

        if j != 0:
            n = j
            slash = '/'
            d = self.denominator
            if i != 0:
                space=' '

        return f'{whole}{space}{n}{slash}{d}'

    def __add__(a,b):
        return MixedFrac(super().__add__(b))
    def __radd__(a,b):
        return MixedFrac(super().__radd__(b))
    def __sub__(a,b):
        return MixedFrac(super().__sub__(b))
    def __rsub__(a,b):
        return MixedFrac(super().__rsub__(b))
    def __mul__(a,b):
        return MixedFrac(super().__mul__(b))
    def __rmul__(a,b):
        return MixedFrac(super().__rmul__(b))
    def __div__(a,b):
        return MixedFrac(super().__div__(b))
    def __rdiv__(a,b):
        return MixedFrac(super().__rdiv__(b))





if TYPE_CHECKING:
    from engine import Engine
    from components.entity import Entity


def check_ap(entity, action):
    if entity.ap < action.COST:
        action.engine.msg("Not enough AP")
        return False
    return True

class Action:
    COST = 0
    def __init__(self, engine: Engine = None, entity: Entity = None) -> None:
        super().__init__()
        self.engine = engine
        self.entity = entity

    def available(self) -> bool:
        return True

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

    def __str__(self):
        return getattr(self, "FLAVOR", super().__str__())


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class FuelAction(Action):
    COST = 0
    def perform(self) -> None:
        self.entity.fuel -= 1
        self.entity.ap += MixedFrac(1,2)
    def available(self) -> bool:
        return self.entity.fuel > 0

class DrinkAction(Action):
    COST = 0
    def perform(self) -> None:
        if self.entity.water > 0:
            self.entity.water -= 1
            self.entity.stamina = min(self.entity.stamina+3, self.entity.max_stamina)
    def available(self) -> bool:
        return self.entity.water > 0

class CampingAction(Action):
    COST = 1

    def __init__(self, engine, entity):
        super().__init__(engine, entity);
        self.loc = self.engine.game_map.get_loc(self.entity.x, self.entity.y)

    def available(self) -> bool:
        loc = self.loc
        if isinstance(loc, locations.Settlement):
            self.engine.msg(f"No camping in town. Move along.")
            return False
        if isinstance(loc, locations.Desert):
            if not hasattr(self.entity, "DESERT_CAMPSITE_TOOLKIT"):
                self.engine.msg(f"Too rough camping on the dunes.")
                return False
        return check_ap(self.entity, self)

    def perform(self):
        v = self.engine.deck.top.value
        entity = self.entity

        recover = 3

        if   v > 12:
            self.engine.msg("At dawn break, you notice moisture trickling down nearby rocks. You collect the dew stream into your canteen")
            entity.water = min(entity.water+1, entity.max_water)
        elif v > 10:
            self.engine.msg("Winds and sand howl outside your tent, tearing at the material. You spend most of the night keeping the tent down.")
            recover = 0
        elif v >  8:
            self.engine.msg("You hear a swish in your fuel tank - a welcome surprise!")
            entity.fuel = min(entity.fuel+1, entity.max_fuel)
        elif v >  6:
            self.engine.msg("A strong smell lingers in the air, distracting and intrusive to your senses.")
            recover = 2
        elif v >  4: # +1 speed next turn => +.5 AP
            self.engine.msg("You take time to tweak your Glider, adjusting it for the weather ahead")
            entity.CAMPING_TWEAK = MixedFrac(1,2)
        else:
            self.engine.msg("Exhaustion creeps across you. You sleep a deep and restful sleep.")
            recover = entity.MAX_STAMINA

        if hasattr(entity, "MEDICAL_PACK"):
            recover += 1

        if hasattr(entity, "SURVIVAL_KNOWLEDGE"):
            recover = entity.MAX_STAMINA

        if hasattr(entity, "PIEZO_CAPTURE"):
            entity.water = min(entity.water+1, entity.max_water)

        if hasattr(entity,"PORTABLE_REPAIR"):
            v = self.engine.deck.top.value
            if v.value >= 10:
                entity.fuel = min(entity.fuel + 1, entity.max_fuel)


        self.engine.msg(f"You spend the night and recover {recover} stamina.")

        entity.stamina = min(entity.stamina+recover, entity.max_stamina)
        entity.ap = 0 #end turn
        entity.fatigue = 0

class MovementAction(Action):
    def __init__(self, engine: Engine, entity: Entity, dx: int, dy: int):
        super().__init__(engine, entity)

        self.dx = dx
        self.dy = dy

        self.COST = MixedFrac(1, 2 * (entity.speed + engine.WEATHER_WIND_BACK))
        if engine.WEATHER_SAND_STORM == 1:
            self.COST *= 2

    def perform(self) -> None:
        entity = self.entity
        entity.move(self.dx, self.dy)
        entity.ap -= self.COST

        if hasattr(entity,"FUEL_RECYCLE"):
            v = self.engine.deck.top.value
            if v.value >= 10:
                entity.fuel = min(entity.fuel + 1, entity.max_fuel)

    def available(self):
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy

        if not self.engine.game_map.is_revealed(dest_x, dest_y):
            if not hasattr(self.entity, "PATHFINDER_TOOLS"):
                return  False
        elif not self.engine.game_map.is_traversable(dest_x, dest_y):
            if not hasattr(self.entity, "PATHFINDER"):
                return False

        return check_ap(self.entity, self)



class PassAction(Action):
    COST = 0
    def perform(self) -> None:
        self.entity.ap = 0


class RevealAction(Action):
    COST = 1
    radius = 1

    def perform(self) -> None:
        loc = locations.draw(self.engine.deck, self.dest_x, self.dest_y)

        map = self.engine.game_map
        map.add_location(loc)

        self.engine.msg(f"You see a {loc} on the horizon.")

        if isinstance(loc, locations.Unique):
            self.entity.fame += MixedFrac(1,2)


        # If large size, add if possible
        tiles = [(loc.x, loc.y)]
        for _ in range(1, loc.size):
            for t in tiles:
                dx,dy = map.nearest_empty(t[0], t[1])
                if dx is None:
                    continue
                map.add_location(loc, x=dx,y=dy)
                tiles.append((dx,dy))
                break
            else: break

        # If deserts, add if possible
        for _ in range(0, loc.desert):
            for t in tiles:
                dx,dy = map.nearest_empty(t[0], t[1], r=3)
                if dx is None:
                    continue
                map.add_location(locations.Desert(dx,dy, deck=self.engine.deck))
                tiles.append((dx,dy))
                break
            else: break


        self.entity.ap -= self.COST

    def available(self) -> bool:

        if self.engine.WEATHER_SPICE_CLOUDS == 1:
            return False

        if not check_ap(self.entity,self):
            return False

        x = self.entity.x
        y = self.entity.y

        map = self.engine.game_map

        r = self.radius + 1 if hasattr(self.entity, "WAYFINDING") else self.radius

        self.dest_x,self.dest_y = map.nearest_empty(x,y,r)

        if self.dest_x is None:
            self.engine.msg(f"Nothing to see here. Move along.")

        return self.dest_x is not None


class ExploreAction(Action):
    COST = 1
    def __init__(self, engine, entity):
        super().__init__(engine, entity)
        self.loc = engine.game_map.get_loc(entity.x, entity.y)
        self.success = False


    def perform(self) -> None:
        encounter = self.loc.explore(self.entity)
        label = encounter.__name__.replace("_", " ").title()
        self.engine.msg(f"Exploring, found a {label}")
        self.result = encounter(self.loc, self.entity, self.engine.deck)
        self.success = not type(self.result) is int
        if self.success:
            self.engine.msg(f"Success! Recieved {self.result}")
            self.loc.xp -= 1
            self.loc.tile = self.loc.tile.copy()
            self.loc.tile["dark"]["ch"] = ord(" ")
            if hasattr(self.entity, "AIR_PURIFIER"):
                self.entity.stamina += 1

        else :
            self.engine.msg(f"Failed by {self.result}")

        self.entity.stamina -= 1
        self.entity.ap -= self.COST
        self.entity.can_explore = False

        if hasattr(self.entity, "THERMAL_UNDERWEAR"):
            self.entity.stamina += 1

    def available(self) -> bool:
        if not self.entity.can_explore:
            self.engine.msg("Limit once per turn.")
            return False

        if not self.loc.can_explore(self.entity):
            self.engine.msg("Not explorable.")
            return False

        if not self.entity.stamina >= 1:
            self.engine.msg("Not enough stamina to explore.")
            return False

        return check_ap(self.entity, self)

class RetryAction(Action):
    COST = 0
    def __init__(self, engine, entity):
        super().__init__(engine, entity)
        self.loc = engine.game_map.get_loc(entity.x, entity.y)
        self.success = False


    def perform(self) -> None:
#        breakpoint()
        encounter = self.loc.explore(self.entity)
        label = encounter.__name__.replace("_", " ").title()
        self.engine.msg(f"Rerolling, at a {label}")

        # set level to # of failures, retry, then reset
        self.loc.level, old = self.last.result, self.loc.level

        result = encounter(self.loc, self.entity, self.engine.deck)

        self.loc.level =  old


        self.success = not type(result) is int
        if self.success:
            self.engine.msg(f"Success! Recieved {result}")
            self.loc.xp -= 1
            self.loc.tile = self.loc.tile.copy()
            self.loc.tile["dark"]["ch"] = ord(" ")
            if hasattr(self.entity, "AIR_PURIFIER"):
                self.entity.stamina += 1
        else :
            self.engine.msg(f"Failed by {result}")

        self.entity.stamina -= 1

    def available(self) -> bool:
        if not len(self.entity.moves) > 0: return False

        self.last = self.entity.moves[-1]
        if not isinstance(self.last, ExploreAction): return False
        if self.last.success: return False

        return self.entity.stamina > 0

### Settlement actions

class VisitAction(Action):
    COST = 1
    def __init__(self, engine, entity):
        super().__init__(engine, entity)
        self.loc = engine.game_map.get_loc(entity.x, entity.y)

    def perform(self) -> None:
        self.engine.msg("You visit the settlement.")

        self.entity.in_town = True
        self.entity.ap -= self.COST
        self.entity.can_visit = False

        actions = dict()

        actions[event.K_r] = RestAction(self.engine, self.entity)
        actions[event.K_f] = FuelMerchant(self.engine, self.entity)
        actions[event.K_w] = WaterMerchant(self.engine, self.entity)
        actions[event.K_s] = SellScrap(self.engine, self.entity)
        actions[event.K_l] = SellRelic(self.engine, self.entity)

        actions[event.K_g] = GuildAction(self.engine, self.entity, self.loc)

        actions[event.K_d] = DonateRelic(self.engine, self.entity)
        actions[event.K_b] = RebuildAction(self.engine, self.entity)
        actions[event.K_y] = HideAction(self.engine, self.entity)

        actions[event.K_x] = SettlementExploreAction(self.engine, self.entity)
        actions[event.K_k] = SkilledLaborerAction(self.engine, self.entity)

        for i, item in enumerate(self.loc.items):
            key = event.K_0 + i + 2
            actions[key] = ShoppingAction(self.engine, self.entity, item, key, self.loc)

        if self.loc.companion:
            actions[event.K_h] = FindCompanionAction(self.engine, self.entity,self. loc)



        self.engine.settlement_actions = {k:v for k,v in actions.items() if v.available()}


    def available(self) -> bool:
        if not self.entity.can_explore:
            self.engine.msg("Limit once per turn.")
            return False
        if not self.loc.can_visit:
            self.engine.msg("Not a settlement.")
            return False
        return check_ap(self.entity, self)

class VisitEndAction(Action):
    def perform(self) -> None:
        #TODO
        self.entity.in_town = False

class RestAction(VisitAction):
    FLAVOR = "Rest and Relax (5 credits)"
    def perform(self) -> None:
        if isinstace(self, Home) and hasattr(self.entity, "MOONDEW_REST_DISCOUNT"):
            if hasattr(self.entity, "MOONDEW_REST_WATER"):
                self.entity.water = min(self.entity.max_water, self.entity.water + 1)
        else :
            self.entity.credits -= 5
        self.entity.stamina = self.entity.max_stamina
        if hasattr(self.entity, "SNACK"):
            self.entity.stamina += 2
        self.engine.settlement_actions.pop(event.K_r)

    def available(self) -> bool:
        if self.entity.stamina >= self.entity.max_stamina: return False #TODO potential bug if gaining water from moondew_rest_water ???
        if isinstace(self, Home) and hasattr(self.entity, "MOONDEW_REST_DISCOUNT"):
            return  True
        return self.entity.credits >= 5

class WaterMerchant(VisitAction):
    def __init__(self,engine, entity):
        super().__init__(engine,entity)
        self.price =  max(engine.deck.heat) // 10
        self.FLAVOR = f"Buy from Water Merchant: 1 water for {self.price} credits"
    def perform(self) -> None:
        self.entity.credits -= self.price
        self.entity.water = self.entity.water + 1
        self.engine.settlement_actions.pop(event.K_w)

    def available(self) -> bool:
        return self.entity.credits >= self.price and self.entity.water < self.entity.max_water

class FuelMerchant(VisitAction):
    def __init__(self,engine, entity):
        super().__init__(engine,entity)
        self.price = 4 + engine.deck.bottom.value % 3
        self.FLAVOR = f"Refuel your Glider: 1 fuel for {self.price} credits"
    def perform(self) -> None:
        self.entity.credits -= self.price
        self.entity.fuel += 1
        if self.entity.fuel == self.entity.max_fuel:
            self.engine.settlement_actions.pop(event.K_f)

    def available(self) -> bool:
        return self.entity.credits >= self.price and self.entity.fuel < self.entity.max_fuel

class ShoppingAction(VisitAction):
    def __init__(self, engine: Engine, entity: Entity, item, key, loc):
        super().__init__(engine, entity)
        self.item = item
        self.key = key
        self.loc = loc
        self.cost = item.cost
        if not item.glider and hasattr(entity, 'EQUIP_DISCOUNT'):
            self.cost -= 25
        if item.glider and hasattr(entity, 'GLIDER_DISCOUNT'):
            self.cost -= 25
        self.FLAVOR = f"Buy {item.name} ({self.cost})"
    def perform(self) -> None:
        if self.entity.credits < self.cost:
            self.engine.msg("Not enough credits")
            return None
        self.engine.msg(f"You buy the {self.item.name}")
        self.engine.settlement_actions.pop(self.key)
        self.entity.credits -= self.cost
        self.item(self.entity)
        self.loc.items = [i for i in self.loc.items if i is not item]
    def available(self) -> bool:
        return True

#TODO
class GuildAction(VisitAction):
    def __init__(self, engine: Engine, entity: Entity, loc):
        super().__init__(engine, entity)
        self.loc = loc
        if self.loc.guild:
            self.FLAVOR = f"Visit the {self.loc.guild.label}."
    def perform(self) -> None:
        self.engine.settlement_actions.pop(event.K_g)
        self.loc.guild.advance(self.entity)
    def available(self) -> bool:
        return self.loc.guild is not None

class SellScrap(VisitAction):
    def __init__(self, engine: Engine, entity: Entity):
        super().__init__(engine, entity)
        self.card = engine.deck.top
        self.price = 5

        if self.card.rank == 'W':
            self.price = 30
        elif self.card.rank == 'K':
            self.price = 25
        elif self.card.value >= 11:
            self.price = 20
        elif self.card.value >= 10:
            self.price = 60
        elif self.card.value >= 6:
            self.price = 40

        self.price += getattr(entity, "CREDIT_DUPLICATOR", 0)

        self.FLAVOR = f"Sell {entity.cargo} cargo at {self.price} each"

    def perform(self) -> None:
        self.amount = self.entity.cargo
        self.entity.credits += self.amount * self.price
        self.entity.cargo = 0

        for i in (event.K_s, event.K_r, event.K_d, event.K_b, event.K_y):
            self.engine.settlement_actions.pop(event.K_s, 0)

    def available(self) -> bool:
        return self.entity.cargo > 0

class SellRelic(VisitAction):
    def __init__(self, engine: Engine, entity: Entity):
        super().__init__(engine, entity)
        self.card = engine.deck.top
        self.limit = 0
        self.price = 0

        if self.card.rank == 'W':
            self.limit = 2
            self.price = 100
        elif self.card.rank == 'K':
            self.limit = 3
            self.price = 80
        elif self.card.rank == 'Q':
            self.limit = 1
            self.price = 100
        elif self.card.value >= 10:
            self.limit = 2
            self.price = 60
        elif self.card.value >= 6:
            self.limit = 2
            self.price = 40

        self.amount = min(self.limit, self.entity.relic)
        self.FLAVOR = f"Sell {self.amount} relics at {self.price} each"

    def perform(self) -> None:
        self.amount = min(self.limit, self.entity.relic)
        self.entity.credits += self.amount * self.price
        self.entity.relic = 0
        if self.card.rank == 'W':
            self.entity.fame += 1

        for i in (event.K_s, event.K_r, event.K_d, event.K_b, event.K_y):
            self.engine.settlement_actions.pop(event.K_s, 0)

    def available(self) -> bool:
        return self.entity.relic > 0 and self.card.value >= 6


class DonateRelic(VisitAction):
    FLAVOR = "Donate relics for preservation."
    def perform(self) -> None:
        r = min(self.entity.relic, 2)
        self.entity.relic -= r
        self.engine.msg(f"You donate {r} relics for preservation.")
        self.entity.fame += MixedFrac(r,2)
        for i in (event.K_s, event.K_r, event.K_d, event.K_b, event.K_y):
            self.engine.settlement_actions.pop(event.K_s, 0)
    def available(self) -> bool:
        if self.entity.x != 0 or self.entity.y != 0: return False # only at Home
        if self.entity.secrecy == 99 or self.entity.restoration == 99: return False
        return self.entity.relic > 0

class RebuildAction(VisitAction):
    FLAVOR = "Rebuild the town. (2 cargo and 50 credits)"
    def perform(self) -> None:
        self.engine.msg("You contribute cargo and cash to the restoration cause.")
        self.entity.cargo -= 2
        self.entity.credits -= 50
        self.entity.restoration += 1
        for i in (event.K_s, event.K_r, event.K_d, event.K_b, event.K_y):
            self.engine.settlement_actions.pop(event.K_s, 0)
    def available(self) -> bool:
        if self.entity.x != 0 or self.entity.y != 0: return False # only at Home
        return self.entity.restoration != 99 and (self.entity.cargo >= 2 or self.entity.credits >= 50)

class HideAction(VisitAction):
    FLAVOR = "Conceal your true identity. (2 relics or 150 credits)"
    def perform(self) -> None:
        if self.entity.relic >= 2:
            self.engine.msg("You stash two relics.")
            self.entity.relic -= 2
            self.entity.secrecy += 1
        elif self.credits >= 150:
            self.engine.msg("You pay a bribe to quiet loose tongues.")
            self.credits -= 150
            self.entity.secrecy += 1
        for i in (event.K_s, event.K_r, event.K_d, event.K_b, event.K_y):
            self.engine.settlement_actions.pop(event.K_s, 0)
    def available(self) -> bool:
        if self.entity.x != 0 or self.entity.y != 0: return False # only at Home
        return self.entity.secrecy != 99 and (self.entity.relic >= 2 or self.entity.credits >= 150)


class FindCompanionAction(VisitAction):

    def __init__(self, engine: Engine, entity: Entity, loc):
        super().__init__(engine, entity)
        self.loc = loc
        self.companion = loc.companion
        if self.companion is not None:
            self.cost = max(0, self.cost - getattr(entity, "COMPANION_DISCOUNT", 0))

            self.FLAVOR = f"Hire {self.companion.name}, a {self.companion.title} for {self.companion.cost} credits."
        if len(self.entity.companions) > 0 :
            self.fire = next(iter(self.entity.companions))
            if self.companion is None:
                self.FLAVOR = f"Fire {self.companion.name}"

    def perform(self) -> None:
        e = self.entity
        if self.companion is None:
            leaving = self.fire
            self.engine.msg(f"{leaving.name} leaves")
            self.loc.companion = leaving
            leaving.leave(e)
            return
        if (e.credits < self.cost:
            self.engine.msg("Not enough credits")
            return None
        if e.fame < len(e.companions) * e.fame_per_companion:
            leaving = self.fire
            self.engine.msg(f"{leaving.name} leaves")
            self.loc.companion = leaving
            leaving.leave(e)
        else:
            self.loc.companion = None

        self.engine.msg(f"{self.companion} joins you")
        self.companion.join(e)

    def available(self) -> bool:
        if self.entity.fame_per_companion == 99: return FAlse
        return self.loc.companion is not None or len(self.entity.companions) > 0

#TODO
class SettlementExploreAction(ExploreAction):
    FLAVOR = "Explore the settlement"
    def perform(self):
        from .settlement_encounters import draw
        encounter = draw(self.engine.deck.top)
        choices = encounter(self.engine, self.entity) or []
        for i, c in enumerate(choices):
            if c.available():
                self.engine.settlement_actions[event.K_6 +i] = c
        self.engine.settlement_actions.pop(event.K_x, 0)
    def available(self) -> bool:
        return True

class SkilledLaborerAction(Action):
    FLAVOR = "Do skilled labor"
    def perform(self):
        self.entity.stamina -= 2
        self.entity.credits += 10
        self.engine.settlement_actions.pop(event.K_k, 0)
    def available(self) -> bool:
        if not hasattr(self.entity, "MOONDEW_LABORER"): return False
        if not self.entity.x ==0 and self.entity.y == 0: return False
        if not self.entity.stamina >= 2: return False
        return True
