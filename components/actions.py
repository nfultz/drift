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
        self.ap += .5


class DrinkAction(Action):
    COST = 0
    def perform(self) -> None:
        if self.entity.water > 0:
            self.entity.water -= 1
            self.entity.stamina = max(self.entity.stamina+3, self.entity.max_stamina)

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




