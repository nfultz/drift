#!/usr/bin/env python3
import logging
import traceback

import tcod


from engine import Engine
from components.entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.


def main() -> None:

    global player_x, player_y
    """Script entry point."""
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "data/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD,
    )
    # Create the main console.
    console = tcod.Console(WIDTH, HEIGHT, order="F")



    player = Entity(int(WIDTH / 2), int(HEIGHT / 2), "@", (255, 255, 255))
    npc = Entity(int(WIDTH / 2 - 5), int(HEIGHT / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(WIDTH, HEIGHT-10)

    engine = Engine(entities=entities, game_map=game_map, player=player)

    # Create a window based on this console and tileset.
    with tcod.context.new(  # New window for a console of size columns×rows.
        columns=console.width, rows=console.height, tileset=tileset,
        title="drift"
    ) as context:
        while True:  # Main loop, runs until SystemExit is raised.
            engine.render(console=console, context=context)

            events = tcod.event.wait()
            engine.event_handler.handle_events(events)


#    with tcod.context.new(
#        columns=80,
#        rows=40,
#        title="drift",
#        vsync=True,
#    ) as context:
#        try:
#            while True:
#                root_console.clear()
#                event_handler.on_render(console=root_console)
#                context.present(root_console)
#
#                try:
#                    for event in tcod.event.wait():
#                        context.convert_event(event)
#                        event_handler = event_handler.handle_events(event)
#                except Exception:  # Handle exceptions in game.
#                    traceback.print_exc()  # Print error to stderr.
#                    # Then print the error to the message log.
#                    if isinstance(event_handler, game.input_handlers.EventHandler):
#                        event_handler.engine.message_log.add_message(traceback.format_exc(), game.color.error)
#        except game.exceptions.QuitWithoutSaving:
#            raise SystemExit()
#        except SystemExit:  # Save and quit.
#            save_game(event_handler, "savegame.sav")
#            raise
#        except BaseException:  # Save on any other error.
#            save_game(event_handler, "savegame.sav")
#            raise
#

if __name__ == "__main__":
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    main()
