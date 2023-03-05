import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

import sortedcontainers

from components import locations

class GameMap:
    def __init__(self, width: int, height: int):
        self.dim = (width, height)

        self.locations = sortedcontainers.SortedDict()

        self.add_location(locations.Home(0,0))
        self.add_location(locations.Desert(0,1))
        self.add_location(locations.Desert(0,-1))
        self.add_location(locations.Desert(1,0))
        self.add_location(locations.Desert(-1,0))
        print(self.locations)

    def render(self, console: Console) -> None:
        tiles = np.full(self.dim, fill_value=tile_types.empty, order="F")

#        tiles[32:33, 22] = tile_types.wall

        top, left, bottom, right = 10, -10, -10, 10
        tiles[0-bottom,0-left] = tile_types.desert

        for y in self.locations.islice(bottom, top):
            for x in self.locations[y].islice(left, right):
                print(x,y)
                tiles[x-bottom,y-left] = tile_types.desert

        console.tiles_rgb[0:self.dim[0], 0:self.dim[1]] = tiles["dark"]

    def add_location(self,loc):
        x, y = loc.x, loc.y
        if not y in self.locations:
            self.locations[y] = sortedcontainers.SortedDict()
        self.locations[y][x] = loc

    def in_bounds(self,x,y):
        return self.is_revealed(x,y)

    def is_revealed(self,x,y):
        return not self.is_empty(x,y)

    def is_empty(self,x,y):
        return not y in self.locations or not x in self.locations[y]
