#!/usr/bin/env python3
import logging
import traceback

import tcod

import sys

import getpass

from engine import Engine
from components import backgrounds
from components.entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.


def main(args) -> None:

    """Script entry point."""
    tileset = tcod.tileset.load_tilesheet(
        "data/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD,
    )
    # Create the main console.
    console = tcod.Console(WIDTH, HEIGHT, order="F")


    if not len(args):
        args.append("n/a")
    bg = getattr(backgrounds, args[0], None)
    if bg: bg = bg()

    player = Entity(0, 0, "@", (255, 255, 255),
            name=getpass.getuser(), background=bg)

    game_map = GameMap(WIDTH-2, HEIGHT-15)

    engine = Engine(entities={player}, game_map=game_map, player=player)

    # Create a window based on this console and tileset.
    with tcod.context.new(  # New window for a console of size columns×rows.
        columns=console.width, rows=console.height, tileset=tileset,
        title="drift"
    ) as context:
        engine.loop(console, context)

if __name__ == "__main__":
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    args = list(sys.argv)
    args.pop(0)
    main(args)
