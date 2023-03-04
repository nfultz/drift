from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from components.entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = EventHandler(self)
        self.game_map = game_map
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in self.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()

