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

        self.top, self.left, self.bottom, self.right = height//2, -width//2, -height//2, width//2

    def center(self, entity) -> None:
        width, height = self.dim
        x, y = entity.x, entity.y

        if x - self.left < width // 4:
#            breakpoint()
            self.left -= width // 4
            self.right -= width // 4
        elif self.right - x < width // 4:
#            breakpoint()
            self.left += width // 4
            self.right += width // 4

        if y - self.bottom < height // 4:
#            breakpoint()
            self.bottom -= height // 4
            self.top -= height // 4
        elif self.top - y < height // 4:
#            breakpoint()
            self.bottom += height // 4
            self.top += height // 4

    def render(self, console: Console) -> None:
        tiles = np.full(self.dim, fill_value=tile_types.empty, order="F")

        for y in self.locations.irange(self.bottom, self.top-1):
            for x in self.locations[y].irange(self.left, self.right-1):
#                print(x,y)
                tiles[x-self.left,y-self.bottom] = self.locations[y][x].tile


        # border
        tiles[0, 0:self.dim[1]] = tile_types.border_left
        tiles[self.dim[0]-1, 0:self.dim[1]] =  tile_types.border_right
        tiles[0:self.dim[0], 0] =  tile_types.border_top
        tiles[0:self.dim[0], self.dim[1]-1] =  tile_types.border_bottom

        width, height = self.dim
        tiles[0, height//4] = tile_types.border_top
        tiles[0, height//2] = tile_types.border_top
        tiles[0,3* height//4] = tile_types.border_top
        tiles[width//4, 0] = tile_types.border_left
        tiles[width//2, 0] = tile_types.border_left
        tiles[3*width//4,0] = tile_types.border_left

        console.tiles_rgb[0:self.dim[0], 0:self.dim[1]] = tiles["dark"]

    def render_entity(self, entity, console: Console) -> None:
        console.print(entity.x -self.left, entity.y -self.bottom, entity.char, fg=entity.color)

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

