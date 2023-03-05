from __future__ import annotations

from typing import TYPE_CHECKING
from fractions import Fraction
from . import locations

if TYPE_CHECKING:
    from engine import Engine
    from components.entity import Entity


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
        self.entity.ap += Fraction(1,2)
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
        return self.entity.water > 0 and self.entity.ap >= self.COST

    def perform(self):
        v = self.engine.deck.top.value
        entity = self.entity

        recover = 3

        if   v > 12:
            entity.water = min(self.entity.water+1, self.entity.max_water)
        elif v > 10:
            recover = 0
        elif v >  8:
            entity.fuel = min(self.entity.fuel+1, self.entity.max_fuel)
        elif v >  6:
            recover = 2
        elif v >  4: #TODO +1 speed next turn
            pass
        else:
            recover = entity.MAX_STAMINA

        entity.stamina = min(self.entity.stamina+recover, self.entity.max_stamina)
        entity.ap = 0 #end turn
        entity.fatigue = 0

class MovementAction(Action):
    def __init__(self, engine: Engine, entity: Entity, dx: int, dy: int):
        super().__init__(engine, entity)

        self.dx = dx
        self.dy = dy

        self.COST = Fraction(1, 2 * entity.speed)

    def perform(self) -> None:
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
#        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
#            return  # Destination is blocked by a tile.

        self.entity.move(self.dx, self.dy)
        self.entity.ap -= self.COST

        loc = self.engine.game_map.locations[self.entity.y][self.entity.x]
        print(f'({loc.x},{loc.y}) {type(loc)}')


class RevealAction(Action):
    COST = 1

    def perform(self) -> None:
        loc = locations.draw(self.engine.deck, self.dest_x, self.dest_y)

        map = self.engine.game_map
        map.add_location(loc)

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
        print(f'({loc.x},{loc.y}) {type(loc)}')

    def available(self) -> bool:

        if self.entity.ap < self.COST:
            return False

        x = self.entity.x
        y = self.entity.y

        map = self.engine.game_map

        self.dest_x,self.dest_y = map.nearest_empty(x,y)
        return self.dest_x is not None


