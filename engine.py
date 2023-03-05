from typing import Set, Iterable, Any

import tcod
from tcod.context import Context
from tcod.console import Console

from components.actions import EscapeAction, MovementAction
from components.entity import Entity
from components.deck import Deck
from components import weather
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], game_map: GameMap, player: Entity):
        self.entities = entities | {player}
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
            console.print(entity.x +10, entity.y +10, entity.char, fg=entity.color)

        context.present(console)

        console.clear()


    def loop(self, console: Console, context: Context):
        deck = self.deck

        while True:  # Main loop, runs until SystemExit is raised.
            self.fatigue = 1
            print("New Day")
            print("DATE)")
            self.weather = weather.draw(deck)
            print(type(self.weather))
            print(deck.drift)
            print(deck.heat)


            for e in self.entities:
                e.ap = 2
                e.fatigue = self.fatigue
                while e.ap > 0:
                    print(f'ap: {e.ap}')
                    self.render(console=console, context=context)

                    if e is self.player:
                        events = tcod.event.wait()
                        self.event_handler.handle_events(events)
                    else:
                        e.ai()

                if e.background:
                    if not e.goal_completed:
                        if e.background.goal(e):
                            e.goal_completed = TRUE
                            e.background.reward(e)

                e.stamina = max(0, e.stamina - e.fatigue)

