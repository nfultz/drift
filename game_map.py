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
        self.title = ''

    def center(self, entity) -> None:
        width, height = self.dim
        x, y = entity.x, entity.y
        self.title = f'{x} {y} ({self.locations[y][x]})'

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
                tiles[x-self.left,y-self.bottom] = self.locations[y][x].tile

        console.tiles_rgb[0:self.dim[0], 3:3+self.dim[1]] = tiles["dark"]
        console.draw_frame(0,3,self.dim[0],self.dim[1], title=self.title, clear=False)

    def render_entity(self, entity, console: Console) -> None:
        console.print(entity.x -self.left, entity.y -self.bottom +3, entity.char, fg=entity.color)

    def add_location(self,loc,*,x=None,y=None):
        if x is None:
            x, y = loc.x, loc.y
        if not y in self.locations:
            self.locations[y] = sortedcontainers.SortedDict()
        self.locations[y][x] = loc

    def is_revealed(self,x,y):
        return self.get_loc(x,y) is not None

    def is_empty(self,x,y):
        return self.get_loc(x,y) is None

    def is_traversable(self,x,y):
        loc = self.get_loc(x,y)
        return loc is not None and loc.traversable

    def get_loc(self,x,y):
        return self.locations[y][x] if y in self.locations and x in self.locations[y] else None

    def nearest_empty(self, x, y,r=1, at_least=0):
        d = 9999
        ret = (None, None)

        for i in range(x-r,x+r+1):
            for j in range(y-r, y+r+1):
                if self.is_revealed(i,j): continue

                new_d = math.dist((x,y), (i,j))

                if new_d > r: continue
                if new_d < at_least: continue

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

