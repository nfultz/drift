from typing import Tuple

from .backgrounds import Background

import datetime

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    MAX_WATER = 6
    MAX_STAMINA = 10
    MAX_FUEL = 6

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int],
            name: str = "<Unnamed>", background: Background = Background(), ai_cls = None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name

        self.moves = list()

        self.ap = 0 #ACTION POINTS

        # Resources
        self.credits = 50
        self.max_stamina = 5
        self.stamina = 2
        self.max_water = 3
        self.water = 1

        # Glider
        self.speed = 1
        self.max_cargo = 5
        self.cargo = 0
        self.max_relic = 5
        self.relic = 0
        self.max_fuel = 3
        self.fuel = 1

        #upgrade counters = if hits 3, 1 fame
        self.speed_upgrade = 0
        self.relic_upgrade = 0
        self.cargo_upgrade = 0
        self.fuel_upgrade = 0

        # win conditon
        self.fame = 0
        self.restoration = 99
        self.secrecy = 99

        self.fame_per_companion = 4
        self.companions = set()

        self.inventory = list()

        #quests
        self.quest_item_label = None
        self.quest = 0
        self.quest_guild = None

        # Background and Stats
        # NB needs to come near end so that base stats are set and can be modified
        self.background = background

        if background:
            self.h = background.h
            self.k = background.k
            self.r = background.r
            background.bonus(self)
            self.goal_completed = False
        else:
            self.h = 2
            self.k = 2
            self.r = 2



        self.birthdate = datetime.date(
                3055,
                datetime.date.today().month,
                datetime.date.today().day
        )

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def skill_test_n(self, skills="hkr", bonus={}):
        n = 0
        for c in skills:
            n = max(n, getattr(self, c, 0) + bonus.get(c, 0))
        return n

    def win_condition(self):
        if self.secrecy != 99:
            self.fame = 0
            return self.secrecy >= 5
        if self.restoration != 99:
            self.fame = 0
            return self.restoration >= 10
        for c in self.companions:
            if c.win(self.relics): return True
        return self.fame >= 10

