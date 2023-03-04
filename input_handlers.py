from __future__ import annotations
from typing import Optional, TYPE_CHECKING


import tcod.event

from actions import Action, EscapeAction, MovementAction

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

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        engine = self.engine
        player = engine.player

        if key == tcod.event.K_UP:
            action = MovementAction(engine, player, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(engine, player, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(engine, player, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(engine, player, dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
