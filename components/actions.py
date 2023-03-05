from __future__ import annotations

from typing import TYPE_CHECKING

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
        self.entity.ap += .5
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
        return self.entity.water > 0

    def perform(self):
        v = self.engine.deck.top.value
        entity = self.entity

        recover = 3

        if   v > 12: pass
            entity.water = min(self.entity.water+1, self.entity.max_water)
        elif v > 10:
            recover = 0
        elif v >  8:
            entity.fuel = min(self.entity.fuel+1, self.entity.max_fuel)
        elif v >  6: pass
            recover = 2
        elif v >  4: pass #TODO +1 speed next turn
        else:
            recover = entity.MAX_STAMINA

        entity.stamina = min(self.entity.stamina+recover, self.entity.max_stamina)
        entity.ap = 0 #end turn
        entity.fatigue = 0

class MovementAction(Action):
    from fractions import Fraction
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
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        self.entity.move(self.dx, self.dy)




