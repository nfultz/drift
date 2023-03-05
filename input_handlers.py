from __future__ import annotations
from typing import Optional, TYPE_CHECKING


import tcod.event

from components.actions import *

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine: Engine):
        self.engine = engine



    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    debug = False
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        engine = self.engine
        player = engine.player

        if self.debug:
            breakpoint()

        if key == tcod.event.K_UP:
            action = MovementAction(engine, player, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(engine, player, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(engine, player, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(engine, player, dx=1, dy=0)

        elif key == tcod.event.K_r:
            action = RevealAction(engine, player)

        elif key == tcod.event.K_c:
            action = CampingAction(engine, player)

        elif key == tcod.event.K_p:
            action = PassAction(engine, player)

        elif key == tcod.event.K_d:
            action = DrinkAction(engine, player)

        elif key == tcod.event.K_f:
            action = FuelAction(engine, player)

        elif key == tcod.event.K_d:
            self.debug = not self.debug

        elif key == tcod.event.K_q:
            action = EscapeAction()


        # validation
        if action and not action.available():
            return None


        # No valid key was pressed
        return action
