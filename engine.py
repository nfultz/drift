from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from components.entity import Entity
from components.deck import Deck
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = EventHandler(self)
        self.game_map = game_map
        self.player = player
        self.deck = Deck().shuffle()

    def handle_enemy_turns(self) -> None:
        for entity in self.entities:
            if entity is self.player:
                continue
            print(f'The {entity.name} wonders when it will get to take a real turn.')


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()


    def loop(self):

        while True:  # Main loop, runs until SystemExit is raised.
            print("New Day")

            while(self.player.ap > 0):
                engine.render(console=console, context=context)

                events = tcod.event.wait()
                engine.event_handler.handle_events(events)
