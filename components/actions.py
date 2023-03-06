from __future__ import annotations

from typing import TYPE_CHECKING
import fractions
from . import locations


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


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class FuelAction(Action): #TODO
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

    def available(self) -> bool:
        # TODO Not on desert w/o gear
        # Not on settlements
        loc = self.engine.game_map.get_loc(self.entity.x, self.entity.y)
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
            pass
        else:
            self.engine.msg("Exhaustion creeps across you. You sleep a deep and restful sleep.")
            recover = entity.MAX_STAMINA

        self.engine.msg(f"You spend the night and recover {recover} stamina.")

        entity.stamina = min(self.entity.stamina+recover, self.entity.max_stamina)
        entity.ap = 0 #end turn
        entity.fatigue = 0

class MovementAction(Action):
    def __init__(self, engine: Engine, entity: Entity, dx: int, dy: int):
        super().__init__(engine, entity)

        self.dx = dx
        self.dy = dy

        self.COST = MixedFrac(1, 2 * entity.speed)

    def perform(self) -> None:
        self.entity.move(self.dx, self.dy)
        self.entity.ap -= self.COST


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

    def perform(self) -> None:
        loc = locations.draw(self.engine.deck, self.dest_x, self.dest_y)

        map = self.engine.game_map
        map.add_location(loc)

        self.engine.msg(f"You see a {loc} on the horizon.")

        if isinstance(loc, location.Unique):
            self.fame += MixedFrac(1,2)


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
                map.add_location(locations.Desert(dx,dy))
                tiles.append((dx,dy))
                break
            else: break


        self.entity.ap -= self.COST

    def available(self) -> bool:

        if not check_ap(self.entity,self):
            return False

        x = self.entity.x
        y = self.entity.y

        map = self.engine.game_map

        self.dest_x,self.dest_y = map.nearest_empty(x,y)

        if self.dest_x is None:
            self.engine.msg(f"Nothing to see here. Move along.")

        return self.dest_x is not None


class ExploreAction(Action):
    COST = 1
    def __init__(self, engine, entity):
        super().__init__(engine, entity)
        self.loc = engine.game_map.get_loc(entity.x, entity.y)


    def perform(self) -> None:
        #TODO
        self.entity.stamina -= 1
        self.entity.ap -= self.COST
        self.entity.can_explore = False

    def available(self) -> bool:
        if not self.entity.can_explore:
            self.engine.msg("Limit once per turn.")
            return False

        if not self.loc.can_explore():
            self.engine.msg("Not explorable.")
            return False

        if not self.entity.stamina > = 1:
            self.engine.msg("Not enough stamina to explore.")
            return False

        return check_ap(self.entity, self)

### Settlement actions

class VisitAction(Action):
    COST = 1
    def __init__(self, engine, entity):
        super().__init__(engine, entity)
        self.loc = engine.game_map.get_loc(entity.x, entity.y)

    def perform(self) -> None:
        #TODO
        self.entity.ap -= self.COST
        self.entity.can_visit = False
    def available(self) -> bool:
        if not self.entity.can_explore:
            self.engine.msg("Limit once per turn.")
            return False
        if not self.loc.can_visit:
            self.engine.msg("Not a settlement.")
            return False
        return True

class RestAction(VisitAction):
    COST = 1
    def perform(self) -> None:
        self.entry.credits -= 5
        self.entry.stamina = self.entry.max_stamina

    def available(self) -> bool:
        return self.entry.credits >= 5 and self.entry.stamina < self.entry.max_stamina

class WaterMerchant(VisitAction):
    COST = 1
    def perform(self) -> None:
        self.entry.credits -= 10
        self.entry.water = self.entry.water + 1

    def available(self) -> bool:
        return self.entry.credits >= 10 and self.entry.water < self.entry.max_water

class FuelMerchant(VisitAction):
    COST = 1
    def perform(self) -> None:
        self.entry.credits -= 5
        self.entry.fuel += 1
    def available(self) -> bool:
        return self.entry.credits >= 5 and self.entry.fuel < self.entry.max_fuel

#TODO
class ShoppingAction(VisitAction):
    def perform(self) -> None:
        pass
    def available(self) -> bool:
        pass

#TODO
class GuildAction(VisitAction):
    def perform(self) -> None:
        pass
    def available(self) -> bool:
        pass

#TODO
class SellScrap(VisitAction):
    def perform(self) -> None:
        pass
    def available(self) -> bool:
        pass

#TODO
class SellRelic(VisitAction):
    def perform(self) -> None:
        pass
    def available(self) -> bool:
        pass

class DonateRelic(VisitAction):
    def perform(self) -> None:
        self.entity.relics -= 2
        self.entity.fame += 1
    def available(self) -> bool:
        return self.entity.relics >= 2

class RebuildAction(VisitAction)
    def perform(self) -> None:
        self.entity.cargo -= 2
        self.entity.credits -= 50:
        self.entity.restoration += 1
    def available(self) -> bool:
        return self.restoration != 99 and self.entity.cargo >= 2 or self.entity.credits >= 50

class HideAction(VisitAction)
    def perform(self) -> None:
        if self.entity.relics >= 2:
            self.entity.relics -= 2
            self.entity.secrecy += 1
        elif self.credits >= 150:
            self.credits -= 150:
            self.entity.secrecy += 1
    def available(self) -> bool:
        return self.secrecy != 99 and self.entity.relic >= 2 or self.entity.credits >= 150


#TODO
class FindCompanionAction(VisitAction):
    def perform(self) -> None:
        pass
    def available(self) -> bool:
        pass
