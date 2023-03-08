from typing import Set, Iterable, Any

import tcod
from tcod.context import Context
from tcod.console import Console

from components.actions import VisitAction, VisitEndAction
from components.entity import Entity
from components.deck import Deck
from components import weather
from game_map import GameMap
from input_handlers import EventHandler

import datetime

class Engine:
    def __init__(self, entities: Set[Entity], game_map: GameMap, player: Entity):
        self.entities = entities | {player}
        self.event_handler = EventHandler(self)
        self.game_map = game_map
        self.player = player
        self.deck = Deck().shuffle()
        self.date = player.birthdate + datetime.timedelta(
                days=365*(self.deck.top.value + 16) +
                      30*self.deck.bottom.value +
                      self.deck.top.value
              )
        self.firstdate = self.date
        self.messages = ['']*5

    def tomorrow(self):
        self.date += datetime.timedelta(days=1)
        return self.date

    def handle_enemy_turns(self) -> None:
        #TODO
        for entity in self.entities:
            if entity is self.player:
                continue
            print(f'The {entity.name} wonders when it will get to take a real turn.')

    def msg(self, string):
        self.messages.append(string)

    @property
    def status_bar(self):
        p = self.player
        name = p.name
        background = type(p.background).__name__
        stats = 'h'*p.h + 'k'*p.k + 'r'*p.r

        return f"{name} ({background}) {stats} : {p.fame} fame, {p.credits} credits"

    @property
    def status_bar2(self):
        p = self.player
        fuel = 'f'*p.fuel + '-'*(p.max_fuel - p.fuel)
        stamina = 's'*p.stamina + '-'*(p.max_stamina - p.stamina)
        water = 'w'*p.water + '-'*(p.max_water - p.water)

        return f"{fuel} {stamina} {water} / AP: {p.ap}"


    def render(self, console: Console, context: Context) -> None:
        self.game_map.center(self.player)
        self.game_map.render(console)
        for entity in self.entities:
            self.game_map.render_entity(entity, console)

        h = self.game_map.dim[1]
        console.print(0, h+1, string=self.status_bar)
        console.print(0, h+2, string=self.status_bar2)

        for i, j in zip(range(4,9), range(-5,0)):
            console.print(0, h+i, string=self.messages[j])


        context.present(console)

        console.clear()

    def render_town(self, console:Console, context:Context):
        w,h = self.game_map.dim
        console.draw_frame(0,0,w-2,h-2, clear=True)
        for i, k in enumerate(self.settlement_actions):
            v = self.settlement_actions[k]
            console.print(1,1+i, f"{chr(k)} - {v}")

        console.print(0,20, self.deck.top)
        console.print(0, h+1, string=self.status_bar)
        console.print(0, h+2, string=self.status_bar2)

        for i, j in zip(range(4,9), range(-5,0)):
            console.print(0, h+i, string=self.messages[j])
        context.present(console)

    def loop(self, console: Console, context: Context):
        deck = self.deck

        while True:  # Main loop, runs until SystemExit is raised.
            self.fatigue = 1
            self.msg("")
            self.msg(self.tomorrow().strftime("=== %A %B %d, %Y ==="))
            weather.reset(self)
            weather.draw(deck)(self)
            self.msg("The drift today is {0}".format(deck.drift))
            self.msg("with a high of {1} and low of {0}".format(*deck.heat))


            for e in self.entities:

                e.can_explore = True
                e.can_visit = True
                e.in_town = False
                e.ap = 2 + getattr(e,"CAMPING_TWEAK", 0)
                e.CAMPING_TWEAK = 0
                e.fatigue = self.fatigue

                while e.ap > 0:
                    self.render(console=console, context=context)

                    if e is self.player:
                        events = tcod.event.wait()
                        self.event_handler.handle_events(events)

                        while e.in_town:
                                self.render_town(console=console, context=context)
                                events = tcod.event.wait()
                                self.event_handler.handle_events(events)




                    else:
                        e.ai()

                if e.background:
                    if not e.goal_completed:
                        if e.background.goal(e):
                            e.goal_completed = True
                            e.background.reward(e)

                e.stamina = max(0, e.stamina - e.fatigue)

                if e.win_condition():
                    raise WinException()

