import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

import sortedcontainers

from components import locations

class GameMap:
    def __init__(self, width: int, height: int):
        self.locations = sortedcontainers.SortedDict()
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.tiles[30:33, 22] = tile_types.wall

        self.add_location(locations.Home(0,0))
        self.add_location(locations.Desert(0,1))
        self.add_location(locations.Desert(0,-1))
        self.add_location(locations.Desert(1,0))
        self.add_location(locations.Desert(-1,0))

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]

    def add_location(loc):
        x, y = loc.x, loc.y
        if not y in self.locations:
            self.locations[y] = sortedcontainers.SortedDict()
        self.locations[y][x] = loc

    def is_empty(x,y):
        return not y in self.locations or not x in self.locations[y]
