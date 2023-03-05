import numpy as np  # type: ignore
from tcod.console import Console

import sortedcontainers
import math
import random

from components import locations, tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.dim = (width, height)

        self.locations = sortedcontainers.SortedDict()

        self.add_location(locations.Home(0,0))
        self.add_location(locations.Desert(0,1))
        self.add_location(locations.Desert(0,-1))
        self.add_location(locations.Desert(1,0))
        self.add_location(locations.Desert(-1,0))

    def render(self, console: Console) -> None:
        tiles = np.full(self.dim, fill_value=tile_types.empty, order="F")

#        tiles[32:33, 22] = tile_types.wall

        top, left, bottom, right = 10, -10, -10, 10

        for y in self.locations.islice(bottom, top):
            for x in self.locations[y].islice(left, right):
#                print(x,y)
                tiles[x-bottom,y-left] = self.locations[y][x].tile

        console.tiles_rgb[0:self.dim[0], 0:self.dim[1]] = tiles["dark"]

    def add_location(self,loc,*,x=None,y=None):
        if x is None:
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

    def nearest_empty(self, x, y,r=1):
        d = 9999
        ret = (None, None)

        for i in range(x-r,x+r+1):
            for j in range(y-r, y+r+1):
                if self.is_revealed(i,j): continue

                new_d = math.dist((x,y), (i,j))

                if new_d > r: continue
                print(f'({x},{y}) => ({i}{j}) / {new_d}')

                if new_d < d:
                    ties = 1
                    ret = (i,j)
                    d = new_d
                elif new_d == d:
                    ties = ties + 1
                    # below is the resovoir sampling size=1
                    if random.randrange(ties) == 1:
                        ret = (i,j)

        return ret

