from typing import Tuple

from background import Background


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    MAX_WATER = 6
    MAX_STAMINA = 10
    MAX_FUEL = 6

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int],
            name: str = "<Unnamed>", background: Background = None, ai_cls = None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name

        self.moves = list()

        self.ap = 0 #ACTION POINTS

        # Background and Stats
        self.background = background

        if background:
            self.h = background.h
            self.k = background.k
            self.r = background.r
            background.bonus(self)
        else:
            self.h = 2
            self.k = 2
            self.r = 2

        # Resources
        self.credits = 50
        self.max_stamina = 5
        self.stamina = 2
        self.max_water = 3
        self.water = 1

        # Glider
        self.max_cargo = 7
        self.max_fuel = 3
        self.fuel = 1
        self.speed = 1



    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

